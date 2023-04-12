#!/usr/bin/python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1269 Setup Python BIST script
#
# File Name: tdc_base_bist_sys_id.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script.
#
# BIST script for accessing FPGA registers. Note register_access.py is 
# imported to access the FPGA registers. The script is run directly on the 
# Talon board in Python stand-alone mode. 
# Test status is output to the Python logger utility.
#
# Date: 23 DEC 2022, developed during PI17
#
# args: <filename>.json and <filename>.ipmap files
#
# Run on talon board as follows:
# root@talon:~# 
#     python3 tdc_base_bist_sys_id.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#
# functions: 
# sys_id() - reads the bitstream, version, and commit registers
#            read-write test on the scratch register
# 
#-----------------------------------------------------------------------------
import sys
from datetime import datetime, timezone
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

import bist_utils

def sys_id(base_sys_id, checker):
    # read the sys_id version registers/fields
    bitstream = base_sys_id.read_field("bitstream")
    logging.info(f"base_sys_id bitstream: 0x{bitstream:X}")
    prerelease = base_sys_id.read_field("prerelease")
    logging.info(f"base_sys_id prerelease: 0x{prerelease:X}")
    patch = base_sys_id.read_field("patch")
    logging.info(f"base_sys_id patch: 0x{patch:X}")
    minor = base_sys_id.read_field("minor")
    logging.info(f"base_sys_id minor: 0x{minor:X}")
    major = base_sys_id.read_field("major")
    logging.info(f"base_sys_id major: 0x{major:X}")
    commit = base_sys_id.read_field("commit")
    logging.info(f"base_sys_id commit: 0x{commit:X}")
    # read/write/check the FPGA System ID module scratch register:
    base_sys_id.write_field("scratch", 0x0000)
    scratch_reg = base_sys_id.read_field("scratch")
    checker.check(scratch_reg == 0x0000, f"base_sys_id scratch: 0x{scratch_reg:04X}")
    base_sys_id.write_field("scratch", 0xA5A5)
    scratch_reg = base_sys_id.read_field("scratch")
    checker.check(scratch_reg == 0xA5A5, f"base_sys_id scratch: 0x{scratch_reg:04X}")
    base_sys_id.write_field("scratch", 0xB5AF)
    scratch_reg = base_sys_id.read_field("scratch")
    checker.check(scratch_reg == 0xB5AF, f"base_sys_id scratch: 0x{scratch_reg:04X}")

def main(base_sys_id):
    # bist_utils.Date().log_timestamp()
    checker = bist_utils.Checker()
    logging.info(f"#---------------------------------------------------------")
    logging.info(f"Talon-DX FPGA BIST testcase results: System ID")
    sys_id(base_sys_id, checker)
    checker.report_log(f"SYS_ID test results")
    return checker



if __name__ == "__main__":
    logging.info("tdc_base_bist_sys_id: __main__")
    import register_access as ra
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sys_json",                   help="The system map json file that details the register sets in the bitstream.")
    parser.add_argument("sys_ipmap",                  help="System map file that maps the VHDL hierarchy to a simpler name.")
    parser.add_argument("--mem",  metavar="DEV_FILE", help="The file to memory map to gain access to the registers. Defaults to /dev/mem", default="/dev/mem")

    args = parser.parse_args()
    
    # run register_access main():
    regsets = ra.main(args.mem, args.sys_json, args.sys_ipmap)
    base_sys_id = regsets.get("base_sys_id")
    
    #-------------------------------------------------------------------------
    # FPGA module BIST tests:
    #-------------------------------------------------------------------------
    # access the FPGA system identification register set
    checker = main(base_sys_id)    