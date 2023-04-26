#!/usr/bin/env python3

import copy
from functools import partial
import importlib
import json
import mmap
import re
from typing import Dict
import logging

from parse import parse
import Pyro5.server

def _uint_to_signed(unsigned:int, width:int) -> int:
    lim = 2**(width-1)
    if unsigned >= lim:
        val = unsigned - 2**width
    else:
        val = unsigned
    if not -lim <= val < lim:
        raise ValueError(f"{val} outside range {-lim} <= val < {lim}")
    return val

def _uint_fm_signed(signed:int, width:int) -> int:
    lim = 2**(width-1)
    if not -lim <= signed < lim:
        raise ValueError(f"{signed} outside range {-lim} <= val < {lim}")
    if signed < 0:
        return signed + 2**width
    return signed

def _uint_to_ufixed(unsigned:int, width:int, int_bits:int=0) -> float:
    return unsigned/2**(width-int_bits)

def _uint_fm_ufixed(ufixed:float, width:int, int_bits:int=0) -> int:
    lim = 2.0**int_bits
    if not 0.0 <= ufixed < lim:
        raise ValueError(f"val {ufixed} outside range 0 <= val < {lim}")
    return int(ufixed * 2**(width-int_bits))

def _uint_to_sfixed(unsigned:int, width:int, int_bits:int=0) -> float:
    return float(_uint_to_signed(unsigned, width)/2**(width-int_bits-1))

def _uint_fm_sfixed(sfixed:float, width:int, int_bits:int=0) -> int:
    lim = 2.0**int_bits
    if not -lim <= sfixed < lim:
        raise ValueError(f"val {sfixed} outside range {-lim} <= val < {lim}")
    return _uint_fm_signed(int(sfixed * 2**(width-int_bits-1)), width)

class pyField:
    def __init__(self, offset, width, reg_offset:int, 
            ftype="natural", repeat:int=1, 
            readable:bool=True, writeable:bool=True, 
            reg_repeat:int=1, reg_byte_width:int=4,
            set_repeat:int=1, set_byte_width:int=4,
            reset=0):
        assert reg_offset >= 0
        self.reg_offset = reg_offset
        assert reg_repeat > 0
        self.reg_repeat = reg_repeat
        self.reg_byte_width = reg_byte_width
        self.set_repeat = set_repeat
        self.set_byte_width = set_byte_width
        assert offset >= 0
        self.offset     = offset
        assert width > 0
        self.width      = width
        assert repeat > 0
        self.repeat     = repeat
        self._total_repeat = self.set_repeat * self.reg_repeat * self.repeat
        self.ftype      = ftype
        if ftype == "boolean":
            self._uint_to_ftype = bool
            self._ftype_to_uint = int
        elif ftype == "natural":
            self._uint_to_ftype = int
            self._ftype_to_uint = int
        elif ftype == "integer":
            self._uint_to_ftype = partial(_uint_to_signed, width=width)
            self._ftype_to_uint = partial(_uint_fm_signed, width=width)
        elif ftype == "ufixed":
            self._uint_to_ftype = partial(_uint_to_ufixed, width=width) #FIXME Add int_bits.
            self._ftype_to_uint = partial(_uint_fm_ufixed, width=width)
        elif ftype == "sfixed":
            self._uint_to_ftype = partial(_uint_to_sfixed, width=width)
            self._ftype_to_uint = partial(_uint_fm_sfixed, width=width)
        else:
            logging.warning(f"Unknown ftype '{ftype}'.")
            self._uint_to_ftype = int
            self._ftype_to_uint = int

        self.readable   = readable
        self.writeable  = writeable
        if isinstance(reset, int):
            self.reset = self._uint_to_ftype(reset)
        else:
            self.reset = reset

    def set_reg_file(self, reg_file):
        self._reg_file = reg_file
        if self.writeable:
            for idx in range(self.repeat):
                self.write(self.reset, idx, shadow_only=True)

    def _indices(self, idx):
        if idx is None and self._total_repeat > 1:
            raise IndexError(f"Field is repeated so requires an index in the range [0:{self._total_repeat-1}]")
        idx = 0 if idx is None else idx
        if not (0 <= idx < self._total_repeat):
            raise IndexError(f"Field index {idx} is out of bounds [0:{self._total_repeat-1}]")
        set_idx = int(idx % self.set_repeat)
        set_rem = idx // self.set_repeat
        reg_idx = set_rem % self.reg_repeat
        reg_rem = set_rem // self.reg_repeat
        fld_idx = int(reg_rem % self.repeat)
        return set_idx, reg_idx, fld_idx

    def write(self, value, idx=None, shadow_only=False):
        if not self.writeable:
            raise ValueError(f'Field is not writeable.')
        set_idx, reg_idx, fld_idx = self._indices(idx)
        addr    = self.reg_offset + reg_idx*self.reg_byte_width + set_idx*self.set_byte_width
        offset  = self.offset + fld_idx * self.width
        mask    = ((1 << self.width)-1)
        uint    = self._ftype_to_uint(value) & mask
        self._reg_file.write(address=addr, value=uint, mask=mask, offset=offset, byte_width=self.reg_byte_width, shadow_only=shadow_only)

    def read(self, idx=None):
        if not self.readable:
            raise ValueError(f'Field is not readable.')
        set_idx, reg_idx, fld_idx = self._indices(idx)
        addr   = self.reg_offset + reg_idx*self.reg_byte_width + set_idx*self.set_byte_width
        offset = self.offset + fld_idx * self.width
        mask = (1 << self.width)-1
        uint = self._reg_file.read(address=addr, offset=offset, mask=mask, byte_width=self.reg_byte_width)
        return self._uint_to_ftype(uint)

class repeater():
    def __init__(self, field):
        self.field = field

    def __getitem__(self, key):
        if 0 <= key < self.field.repeat:
            return self.field.read(key)
        raise IndexError(f"Index {key} outside of range 0:{self.field.repeat}")

    def __setitem__(self, key, value):
        if 0 <= key < self.field.repeat:
            return self.field.write(value, key)
        raise IndexError(f"Index {key} outside of range 0:{self.field.repeat}")

    def __len__(self):
        return self.field.repeat


def _decode_name(name: str):
    try:
        n, i = name.rsplit("_", 1)
        idx = int(i)
        return n, idx
    except ValueError:
        pass
    return name, None

@Pyro5.server.expose
class RegFile(object):
    _version = ""
    _size = 0
    _fields = {}

    def __init__(self, name, base_address, filename="", desc=None):
        # logging.info(f"Initialising: {name} : {self.__class__} @ 0x{base_address:08X}")
        logging.debug(f"Initialising: {name} : {self.__class__} @ 0x{base_address:08X}")
        self._reg_file = None
        self._page_offset = 0
        self._desc = desc
        # Open the Physical Memory File
        if filename is not None and len(filename):
            self._page_offset  = base_address % mmap.PAGESIZE
            self._page_address = base_address - self._page_offset
            length = self._size + self._page_offset 
            with open(filename, 'r+b') as _f:
                self._reg_file = memoryview(mmap.mmap(_f.fileno(), length=length, offset=self._page_address))
        else:
            self._page_offset  = 0
            self._page_address = base_address
            self._reg_file     = bytearray(self._size)

        self._page_shadow = bytearray(self._page_offset + self._size)
        self._field_instances = {}
        for name, fld in self._fields.items():
            fld_inst = copy.deepcopy(fld)
            fld_inst.set_reg_file(self)
            self._field_instances[name] = fld_inst

        self.__dict__.update(self._field_instances)
        # self.__dict__.update(self._regs)

    def fields(self):
        return self._field_instances.keys()

    def write_field(self, name, value, idx=None, shadow_only=False):
        self._field_instances[name].write(value, idx, shadow_only)
    
    def read_field(self, name, idx=None):
        return self._field_instances[name].read(idx)

    def _memview(self, byte_width):
        if byte_width == 1:
            return self._reg_file.cast('B')
        if byte_width == 2:
            return self._reg_file.cast('H')
        if byte_width == 4:
            return self._reg_file.cast('I')
        if byte_width == 8:
            return self._reg_file.cast('Q')
        raise ValueError(f"Unsupported byte width ({byte_width}) for memory access.")

    def read(self, address:int, offset:int=0, mask:int=-1, byte_width:int=4, shadow=False) -> int:
        lo = self._page_offset + ((address + byte_width - 1) // byte_width) * byte_width
        hi = lo + byte_width
        if shadow:
            value = int.from_bytes(self._page_shadow[lo:hi], 'little')
        else:
            mv = self._memview(byte_width)
            value_le = int(mv[lo//byte_width])
            # value = int.from_bytes(value_le.to_bytes(byte_width, 'little'), 'big')
            value = value_le
            # value = (int.from_bytes(self._reg_file[lo:hi], 'little') >> offset) & mask
        logging.debug(f"READ : 0x{address:X}, {byte_width}, {self._page_address:X} + {lo:X} : {offset}b => 0x{value:0{byte_width*2}X}")
        value = (value >> offset) & mask
        return value

    def write(self, address:int, value:int, mask:int=-1, offset:int=0, byte_width:int=4, shadow_only=False) -> None:
        lo = self._page_offset + ((address + byte_width - 1) // byte_width) * byte_width
        hi = lo + byte_width
        val = int.from_bytes(self._page_shadow[lo:hi], 'little')
        msk = int(mask) << offset
        val &= ~msk
        val |= (value << offset) & msk
        byte_val = val.to_bytes(byte_width, 'little')
        self._page_shadow[lo:hi] = byte_val
        if not shadow_only:
            logging.debug(f"WRITE: 0x{address:X}, {byte_width}, {self._page_address:X} + {lo:X} : {offset}b <= 0x{val:0{byte_width*2}X}")
            val_be = int.from_bytes(byte_val, 'little')
            mv = self._memview(byte_width)
            mv[lo//byte_width] = val_be

    def __setattr__(self, name, value):
        # Default behaviour for class variables.
        if (name.startswith('_')):
            super().__setattr__(name, value)
            return
        # Try to write the field, this is what most accesses will be
        n, idx = _decode_name(name)
        field = self._field_instances.get(n)
        if isinstance(field, pyField):
            if idx is None and field.repeat > 1:
                return repeater(field)
            field.write(value, idx)
            return

        # # Otherwise to write to the register by name
        # reg = self._regs.get(n)
        # if isinstance(reg, dict):
        #     if reg['write']:
        #         self._reg_file[reg] = value
        #     else:
        #         raise ValueError(f'Register "{name}" is not writeable.')
        #     return
        # if isinstance(reg, list):
        #     raise KeyError(f"Repeated register, please provide an index in the range 0:{len(reg)}.")

        # didn't find name in _field_instances or _regs.
        super().__setattr__(name, value)

    def __getattribute__(self, name):
        # Default behaviour for class variables.
        if (name.startswith('_')):
            return super().__getattribute__(name)

        # Try to access the field, this is what most accesses will be.
        n, idx = _decode_name(name)
        field = self._field_instances.get(n)
        if isinstance(field, pyField):
            if idx is None and field.repeat > 1:
                return repeater(field)
            return field.read(idx)

        # # Otherwise read the register by name
        # reg = self._regs.get(name)
        # if isinstance(reg, dict):
        #     if reg['read']:
        #         return self._reg_file[reg]
        #     raise ValueError(f'Register "{name}" is not readable.')

        return super().__getattribute__(name)

    def __str__(self) -> str:
        return str(self._reg_file)

def translate_hierarchy(fpga_instances:Dict, sysmap_filename):

    sysmap_re = re.compile(r"\s*(?P<hierarchy>\S*)?\s*=>\s*(?P<name>[^\s@]*)\s*(@\s*(?P<reg>\S*))?\s*")

    rules = {}
    if sysmap_filename is not None:
        logging.debug(f"Processing {sysmap_filename} as a IPMAP input file.")
        with open(sysmap_filename, 'r') as f:
            for line_cnt, line in enumerate(f.readlines(), start=1):
                line = line.rsplit("#")[0]  # Strip comments to the end of the line.
                rule_str = line.strip()  # strip remaining white space before and after lines.
                if len(rule_str) == 0:   # ignore empty lines
                    continue
                logging.debug(f"rule: {sysmap_filename}:{line_cnt}:{rule_str}")
                match = sysmap_re.search(rule_str)
                if match is None:
                    logging.warning(f"Could not decode: {sysmap_filename}:{line_cnt}:`{rule_str}`")
                    continue
                logging.debug("RegEx result: " + str(match.groupdict()))
                parts = match.groupdict()
                hierarchy_template = parts['hierarchy'].replace(':', '|').replace(".", "|") # correct simulation output to be like synthesis output. modelsim uses : instead of | to separate hierarchy
                if len(hierarchy_template):
                    rules[hierarchy_template] = (parts['name'], parts['reg'])

    named_instances = {}
    for instance, soc_mod in fpga_instances.get("DeTrI", {}).items():
        # Search for a rule that matches the instance's hierarchy.
        for template, rule in rules.items():
            match = parse(template, instance)
            if match:
                logging.debug(f"Instance: {instance} matches template {template}")
                ip_name  = rule[0].format(*match.fixed, **match.named)
                reg_name = rule[1].format(*match.fixed, **match.named) if rule[1] is not None else None
                break
        else:
            ip_name = soc_mod.get('regdef', {}).get("mnemonic", "no_regdef") + str(len(named_instances))
            reg_name = "FIXME"
            logging.warning(f"Instance: '{instance}' did not match a templated name rule, assigning to '{ip_name}'")
        ip_name  = ip_name if reg_name is None else ip_name + '__' + reg_name
        named_instances[ip_name] = soc_mod

    return named_instances


def main(mem_map_filename="", sysmap_filename="/lib/firmware/talon_dx-tdc_base-tdc_vcc_processing.json", sys_ipmap=None):
    with open(sysmap_filename, 'r') as f:
        data = json.load(f)
    # 'data' is a dict with FPGA-hierarchy as keys.
    # translate FPGA hierarchy to simple software names using the .IPMAP file(s)
    named = translate_hierarchy(data, sys_ipmap)
    regsets = {}
    for reg_name, regset in named.items():
        mnemonic = regset.get("regdef", {}).get('mnemonic', None)
        if mnemonic is None:
            logging.debug(f'No register definition for "{reg_name}".')
            continue
        base_addr = regset.get("bridge_address") + regset.get("firmware_offset")
        imp = importlib.import_module('py_reg_sets.'+ mnemonic, '.')
        reg_class = getattr(imp, mnemonic+'_regs')
        pyname = reg_name.replace("/", "__").replace("-", "_")
        instance = reg_class(pyname, base_addr, mem_map_filename, desc=regset)
        if instance._version != regset.get("regdef").get("version"):
            logging.error(f"Instance '{pyname}' has version '{instance._version}' from '{imp}' which is different to the firmware version '{regset.get('regdef').get('version')}'. Continuing bravely.")
        regsets[pyname] = instance

    return regsets

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sys_json",                   help="The system map json file that details the register sets in the bitstream.")
    parser.add_argument("sys_ipmap",   nargs="?",     help="System map file that maps the VHDL hierarchy to a simpler name.", default=None)
    parser.add_argument("--mem",  metavar="DEV_FILE", help="The file to memory map to gain access to the registers. Defaults to /dev/mem", default="/dev/mem")
    parser.add_argument("--pyro", metavar="HOSTNAME", help="Run a Pyro server and expose register sets with HOSTNAME_ prepended.")
    parser.add_argument("--host", metavar="HOSTNAME", help="Hostname or IP address from which to export Pyro objects.", default='localhost')
    parser.add_argument('--log', choices=("debug", "info", "warning", "error"), help="Logging output level.", default="warning")

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper(), logging.WARNING))
    
#    regsets = main("", args.sysmap_json, args.sys_ipmap)
    regsets = main(args.mem, args.sys_json, args.sys_ipmap)
    locals().update(regsets)

    if args.pyro is not None:
        print(f"Starting Pyro Server for {args.pyro}_* at {args.host}.")
        pyro_objs = {obj: f"{args.pyro}_{name}" for name, obj in regsets.items()}
        Pyro5.server.serve(pyro_objs, host=args.host, verbose=args.log=='debug')