#!/bin/sh
# 
# $1: log_filename <filename_log>.txt

clear

echo "log_filename: $1"
rm tdc_base_bist_logfile.txt  

# remove the old log-file if it exists
if [ $1 -eq 0 ]; then
    echo "enter a log filename"
fi

# Run Talon DX FPGA BIST tests.
echo "Running Talon FPGA BIST testcases ..."
# python3 run_bist_tests.py ./talon_dx-tdc_base-tdc_vcc_processing.json ./tdc.ipmap
python3 run_bist_tests.py ./talon_dx-tdc_base.json ./tdc.ipmap
echo ""