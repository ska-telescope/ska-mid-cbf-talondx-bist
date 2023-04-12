#!/usr/bin/env python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1269 Setup Python BIST script
#
# File Name: run_bist_tests.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script library.
#
# This script creates arguments that are read by the Talon Python BIST script.
# Each testcase within the the testcases list is then run individually in a 
# for-loop by the Talon BIST script.
#
# Date: 10 FEB 2023, developed during PI17
#
# usage: e.g running on talon6 
# args: <filename>.json and <filename>.ipmap files
# root@talon6:~/bin_bist# 
#     python3 run_bist_tests.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#-----------------------------------------------------------------------------
import sys
import pathlib
import yaml

import logging
logging_to_file = True

if logging_to_file:
    logfile_name = 'tdc_base_bist_logfile.txt'
    logging.basicConfig(filename=logfile_name, level=logging.INFO)
    print(f"\nLogging Talon FPGA BIST testcase results to file: {logfile_name}")
else:
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    # logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
    # logging.basicConfig(stream=sys.stdout, level=logging.ERROR)


if __name__ == "__main__":
    logging.info("run_bist_tests: __main__")

    # BIST test script arguments dictionary:
    args = dict(
        testcases = [
        "Talon_Status",
        ],
        slim_runtime = 1.0,  # test time in seconds
        # SLIM Transceiver PHYS
        # board: [talon]
        # mbos: SLIM MBO [1:5]
        # channels: MBO [1:4] channels [0..11], MBO [5] channels [0..7]
        slim_xcvr_phys = [
            {
                "board": "talon",
                "mbos": [1, 2, 3, 4, 5,],
                "channels": [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                              [0, 1, 2, 3, 4, 5, 6, 7,], ],
            },  
        ],
        Eth_100G_runtime = 1.0,    # test time in seconds
        Eth_100G_IP_cores = [
            {
                "board": "talon", 
                "Eth_100Gs": [0, 1],
            },
        ],
    )

    # slim_runtime = 360    # BER test time in seconds
    # slim_runtime = 60    # BER test time in seconds
    # slim_runtime = 10.5    # BER test time in seconds
    slim_runtime = 2.5    # BER test time in seconds
    # slim_runtime = 1    # BER test time in seconds
    # slim_runtime = 0.5    # BER test time in seconds
    # slim_runtime = 0    # BER test time in seconds
    args["slim_runtime"] = slim_runtime

    # configure multiple boards to generate and transport frequency slices over SLIM
    slim_xcvr_phys = [
        {
            "board": "talon",

            # "mbos": [1, 2, 4],    # tdc_base FPGA build
            # "channels": [ [0, 1, 2, 3,], [4, 5, 6, 7], [8, 9, 10, 11,], ],

            # "mbos": [1, 3,],      # tdc_vcc_processing FPGA build
            # "channels": [ [0, 1, 2, 3,], 
            #               [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,], ],

            # "mbos": [3,],      # tdc_vcc_processing FPGA build
            # "channels": [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,], ],

            "mbos": [1, 2, 3, 4, 5,],
            "channels": [   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,],
                            [0, 1, 2, 3, 4, 5, 6, 7,], ],
        },  
    ]
    args["slim_xcvr_phys"] = slim_xcvr_phys

    # Eth_100G_runtime = 5.0    # test time in seconds
    # Eth_100G_runtime = 2.5    # test time in seconds
    Eth_100G_runtime = 1.0    # test time in seconds
    # Eth_100G_runtime = 0.5    # test time in seconds
    # Eth_100G_runtime = 0    # test time in seconds

    args["Eth_100G_runtime"] = Eth_100G_runtime

    # Low Latency 100G Ethernet FPGA IP Core
    Eth_100G_IP_cores = [
        {
            'board': "talon", 
            "Eth_100Gs": [0, 1],
            # "Eth_100Gs": [0, ],
        },
    ]
    args["Eth_100G_IP_cores"] = Eth_100G_IP_cores

    # extended list of testcases to be run
    testcases = [   # power-on self-test
        "SYS_ID",
        "Talon_Status",
        "SLIM XCVR Int_LB",
        "100G Ethernet Int_LB",
        # "SLIM XCVR Ext_LB",
        # "100G Ethernet Ext_LB",
    ]
    args["testcases"] = testcases

    logging.info(f"BIST testcase arguments: {args}")

    # write BIST testcase arguments to file: args.yaml
    args_yaml = pathlib.Path("args.yaml")
    with open(args_yaml, "w", encoding="utf-8") as f:
        yaml.dump(args, f)

    # execute the BIST test script: tdc_base_bist.py
    bist_script_name = "tdc_base_bist.py"
    with open(bist_script_name, 'r') as f:
            logging.info(f"Executing {bist_script_name} BIST script testcases.")
            exec(f.read())       
