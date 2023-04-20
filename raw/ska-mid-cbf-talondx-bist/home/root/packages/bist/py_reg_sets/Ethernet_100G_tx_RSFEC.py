from register_access import pyField, RegFile

class Ethernet_100G_tx_RSFEC_regs(RegFile):
    _version = "19.2.0"
    _size = 32
    _fields = {
        "tx_rsfec_revid" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "tx_rsfec_scratch" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "tx_rsfec_name_0" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "tx_rsfec_name_1" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "tx_rsfec_name_2" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "err_ins_all" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "err_ins_single" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "group_num" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "bit_mask" :
            pyField( offset= 8, ftype='natural', width=10, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "sym_32" :
            pyField( offset=24, ftype='boolean', width= 1, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "symbol_err_mask" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        }