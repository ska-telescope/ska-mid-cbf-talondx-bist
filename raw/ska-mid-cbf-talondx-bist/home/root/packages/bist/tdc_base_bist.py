#!/usr/bin/python3
#
#--------------------------------------------------------------------------------
# File Name: tdc_base_bist.py
#
# 
# Description: Python Built-In Self Test (BIST) talon board verification script.
# BIST script for accessing FPGA registers while running on the talon board directly.
# Note register_access.py is imported to access the FPGA registers; the script is 
# run in Python stand-alone instead of running in the Pyro5 /Jupyter Notebook 
# network-based test environment.
#
# Date: 23 DEC 2022, developed during PI17
#
# Run on talon board as follows:
# args: <filename>.json and <filename>.ipmap files
# root@talon:~# python3 tdc_bist.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#--------------------------------------------------------------------------------
import sys
import yaml

import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

import bist_utils
import tdc_base_bist_sys_id
import tdc_base_bist_talon_status
import tdc_base_bist_ethernet
import tdc_base_bist_slim 

if __name__ == "__main__":
    bist_utils.Date().log_timestamp()
    logging.info("tdc_base_bist: __main__")

    import register_access as ra
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sys_json",                   help="The system map json file that details the register sets in the bitstream.")
    parser.add_argument("sys_ipmap",                  help="System map file that maps the VHDL hierarchy to a simpler name.")
    parser.add_argument("--mem",  metavar="DEV_FILE", help="The file to memory map to gain access to the registers. Defaults to /dev/mem", default="/dev/mem")

    args = parser.parse_args()
    # run register_access main() to acquire regsets:
    regsets = ra.main(args.mem, args.sys_json, args.sys_ipmap)

    # BIST arguments (default)
    args = dict(
        testcases = [
            "Talon_Status",
        ],
        slim_runtime = 1.0,          # test time in seconds
        # SLIM Transceiver PHYS:
        slim_xcvr_phys = [
        {
            'board': "talon", 
            "mbos": [1, ],  
            "channels": [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,], ],
        },
        ],
        Eth_100G_runtime = 1.0,    # test time in seconds
        # Low Latency 100G Ethernet FPGA IP Core
        Eth_100G_IP_cores = [
        {
            'board': "talon", 
            "Eth_100Gs": [0, 1],
        },
        ],
    )

    # Overwite default args with those in the file args.yaml
    script_conv = False
    try:
        with open('args.yaml', 'r') as fid:
            args.update(yaml.safe_load(fid))
            logging.info("tdc_base_bist.py: agruments loaded from input file args.yaml")
            script_conv = True
    except:
        FileNotFoundError
        logging.info("Arguments loaded from defaults in script (tdc_bist_script)")

    testcases = args.get("testcases")
    slim_runtime = args.get('slim_runtime')
    slim_xcvr_phys = args.get('slim_xcvr_phys') 
    Eth_100G_runtime = args.get('Eth_100G_runtime')
    Eth_100G_IP_cores = args.get('Eth_100G_IP_cores') 

    #-------------------------------------------------------------------------
    # FPGA module BIST testcases:
    #-------------------------------------------------------------------------
    for testcase in testcases:
        print(f"\nRunning Talon-DX FPGA BIST testcase: {testcase}.")

        # System Identification 
        if testcase == "SYS_ID":
            base_sys_id = regsets.get("base_sys_id")
            checker = tdc_base_bist_sys_id.main(base_sys_id)
            checker.report_print(f"System Identification test results")

        # Talon Status
        if testcase == "Talon_Status":
            talon_status = regsets.get("talon_status")
            checker = tdc_base_bist_talon_status.main(talon_status)
            checker.report_print(f"Talon Status test results")

        # 100G Ethernet (loopback mode: Rx serial (internal))
        if testcase == "100G Ethernet Int_LB":
            eth_phy_loopback_mode = 1
            checker = tdc_base_bist_ethernet.main(Eth_100G_IP_cores, eth_phy_loopback_mode, Eth_100G_runtime, regsets)
            checker.report_print(f"100G Ethernet internal loopback test results")

        # 100G Ethernet (loopback mode: external)
        if testcase == "100G Ethernet Ext_LB":
            eth_phy_loopback_mode = 0
            checker = tdc_base_bist_ethernet.main(Eth_100G_IP_cores, eth_phy_loopback_mode, Eth_100G_runtime, regsets)
            checker.report_print(f"100G Ethernet external loopback test results")

        # SLIM XCVR (loopback mode: Rx serial (internal))
        if testcase == "SLIM XCVR Int_LB":
            slim_xcvr_phy_loopback_mode = 1
            checker = tdc_base_bist_slim.main(slim_xcvr_phys, slim_xcvr_phy_loopback_mode, slim_runtime, regsets)
            checker.report_print(f"SLIM internal loopback test results")

        # SLIM XCVR (loopback mode: external)
        if testcase == "SLIM XCVR Ext_LB":
            slim_xcvr_phy_loopback_mode = 0
            checker = tdc_base_bist_slim.main(slim_xcvr_phys, slim_xcvr_phy_loopback_mode, slim_runtime, regsets)
            checker.report_print(f"SLIM external loopback test results")
