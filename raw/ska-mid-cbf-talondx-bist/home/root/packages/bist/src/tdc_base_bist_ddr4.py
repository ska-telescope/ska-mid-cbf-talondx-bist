#!/usr/bin/python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1285 Report DDR4 BIST status parameters as part of BIST script
#
# File Name: tdc_base_bist_ddr4.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script - DDR4.
#
# BIST script for accessing FPGA registers. Note register_access.py is 
# imported to access the FPGA registers. The script is run directly on the 
# Talon board in Python stand-alone mode. 
# Test status is output to the Python logger utility.
#
# Date: 29 MAR 2023, developed during PI18
#
# args: <filename>.json and <filename>.ipmap files
#
# Run on talon board as follows:
# root@talon:~# 
#     python3 tdc_base_bist_ddr4.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#
# functions: 
# 
# References:
#
#-----------------------------------------------------------------------------
import sys
import time
import yaml
import tqdm
from beautifultable import BeautifulTable
import random
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

import bist_utils

class DDR4_TESTER:
    def __init__(self, regsets, ddr4_tester_name, mem_size, checker) -> None:
        self.ddr4_tester = regsets.get(ddr4_tester_name) 
        self.ddr4_size = mem_size
        self.ddr4_tester_name = ddr4_tester_name
        self.checker = checker
        self.test_status = "init"

    def check_ver_id_reg(self):
        # VER_ID: bits[31:0]
        # DDR4 tester instance version identifier register
        id_reg = self.ddr4_tester.read_field("ver_id")
        self.checker.check(id_reg == 0xFF140423, f"{self.ddr4_tester_name} VER_ID: 0x{id_reg:08X}")

    def reset(self, val=False):
        # Reset: bits[0]:
        # Set this bit to control the DDR4 in reset state.
        self.ddr4_tester.write_field("reset", val) 
        logging.debug(f"{self.ddr4_tester_name} reset: {val}")

    def read_pattern_select_reg(self, pattern):
        # Pattern Select: bits[1:0]
        # Selects the block test pattern
        ddr4_tester_reg = self.ddr4_tester.read_field("pattern_sel") 
        logging.debug(f"{self.ddr4_tester_name} pattern_sel: {ddr4_tester_reg}")
        return ddr4_tester_reg

    def read_block_test_enable_reg(self):
        # Block Test Enable, bits[0]
        # Set this bit to enable the test pattern block test
        ddr4_tester_reg = self.ddr4_tester.read_field("block_test_enable") 
        logging.info(f"{self.ddr4_tester_name} block_test_enable: {ddr4_tester_reg}")

    def write_block_test_enable_reg(self, val=False):
        # Block Test Enable, bits[0]
        # Set this bit to enable the test pattern block test
        self.ddr4_tester.write_field("block_test_enable", val) 

    def check_block_test_status(self, val=False):
        # Test Status: bits[0]        
        # DDR4 test status: 0 = manual, 1 = block 
        ddr4_tester_reg = self.ddr4_tester.read_field("status")
        self.checker.check(ddr4_tester_reg == val, f"{self.ddr4_tester_name} status: {ddr4_tester_reg}")

    def configure_block_test(self, pattern=0, start_addr=0x00000000, stop_addr=0x01000000):
            # initialize block test parameters
            self.write_start_addr_reg(start_addr)
            self.write_stop_addr_reg(stop_addr) 
            logging.debug(f"Initializing block test.")
            self.reset_sequence()
            time.sleep(0.1)
            # configure block test parameters
            logging.debug(f"Configuring block test.")
            self.ddr4_tester.write_field("pattern_sel", pattern)
            self.ddr4_tester.write_field("block_test_enable", True) 
            # self.check_block_test_status(True)

    def check_block_pattern_test_status(self):
        # Check Start: bits[0]
        # DDR4 Tester data checker running status
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_start") 
        self.checker.check_quiet(ddr4_tester_reg == True, f"{self.ddr4_tester_name} chk_start: {ddr4_tester_reg}")

        # Check Done: bits[0]
        # DDR4 Tester data checker finished status
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_done") 
        self.checker.check_quiet(ddr4_tester_reg == True, f"{self.ddr4_tester_name} chk_done: {ddr4_tester_reg}")

        # Check Status: bits[7:0]
        # DDR4 Tester data checker test status, pass = 0xFF
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_status") 
        self.checker.check_quiet(ddr4_tester_reg == 0xFF, f"{self.ddr4_tester_name} chk_status: 0x{ddr4_tester_reg:02X}")

        # Check Error Count: bits[31:0]
        # DDR4 Tester data checker error count, pass = 0x00000000
        ddr4_tester_reg = self.ddr4_tester.read_field("err_cnt") 
        self.checker.check_quiet(ddr4_tester_reg == 0x00000000, f"{self.ddr4_tester_name} err_cnt: {ddr4_tester_reg}")

        # Check Error Address: bits[31:0]
        # DDR4 Tester data checker error address, pass = 0x00000000
        # Note this is the address of last posted error, resets to address 0x00000000
        ddr4_tester_reg = self.ddr4_tester.read_field("err_addr") 
        self.checker.check_quiet(ddr4_tester_reg == 0x00000000, f"{self.ddr4_tester_name} err_addr: 0x{ddr4_tester_reg:08X}")

    def read_check_start_reg(self):
        # Check Start: bits[0]
        # DDR4 Tester data checker running status
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_start") 
        return ddr4_tester_reg

    def read_check_done_reg(self):
        # Check Done: bits[0]
        # DDR4 Tester data checker finished status
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_done") 
        return ddr4_tester_reg

    def read_current_wr_addr_reg(self):
        # Write Address: bits[31:0]
        # DDR4 Tester block test write address
        ddr4_tester_reg = self.ddr4_tester.read_field("wr_addr")
        logging.info(f"wr_addr: 0x{ddr4_tester_reg:08X}")
        return ddr4_tester_reg

    def read_current_rd_addr_reg(self):
        # Read Address: bits[31:0]
        # DDR4 Tester block test read address
        ddr4_tester_reg = self.ddr4_tester.read_field("rd_addr")
        return ddr4_tester_reg

    def read_start_addr_reg(self):
        # Start Address: bits[31:0]
        # DDR4 Tester block test start address
        ddr4_tester_reg = self.ddr4_tester.read_field("start_addr")
        return ddr4_tester_reg

    def write_start_addr_reg(self, val=0x00000000):
        # Start Address: bits[31:0]
        # DDR4 Tester block test start address
        self.ddr4_tester.write_field("start_addr", val)

    def read_stop_addr_reg(self):
        # Start Address: bits[31:0]
        # DDR4 Tester block test stop address
        ddr4_tester_reg = self.ddr4_tester.read_field("stop_addr")
        return ddr4_tester_reg

    def write_stop_addr_reg(self, val=0x00000000):
        # Start Address: bits[31:0]
        # DDR4 Tester block test stop address
        self.ddr4_tester.write_field("stop_addr", val)

    def read_check_status_reg(self):
        # Check Status: bits[7:0]
        # DDR4 Tester data checker test status, pass = 0xFF
        ddr4_tester_reg = self.ddr4_tester.read_field("chk_status") 
        return ddr4_tester_reg

    def read_error_count_reg(self):
        # Check Error Count: bits[31:0]
        # DDR4 Tester data checker error count, pass = 0x00000000
        ddr4_tester_reg = self.ddr4_tester.read_field("err_cnt") 
        return ddr4_tester_reg

    def read_error_addr_reg(self):
        # Check Error Address: bits[31:0]
        # DDR4 Tester data checker error address, pass = 0x00000000
        # Note this is the address of last posted error, resets to address 0x00000000
        ddr4_tester_reg = self.ddr4_tester.read_field("err_addr") 
        return ddr4_tester_reg

    def write_addr_coarse_reg(self, val=0x00000000):
        # Coarse Address: bits[31:0]
        # Coarse address for memory spot check
        self.ddr4_tester.write_field("spot_addr_coarse", val) 

    def write_addr_fine_reg(self, val=0x00000000):
        # Fine Address: bits[4:0]
        # Fine address for memory spot check
        self.ddr4_tester.write_field("spot_addr_fine", val) 

    def write_data_reg(self, val=0x00000000):
        # Write Data : bits[31:0]
        # Write data for for memory spot check
        self.ddr4_tester.write_field("spot_write_data", val) 
        
    def read_data_reg(self):
        # Read Data : bits[31:0]
        # Read data for for memory spot check
        ddr4_tester_reg = self.ddr4_tester.read_field("spot_read_data") 
        return ddr4_tester_reg

    def rw_enable(self, val=1):
        # Read/Write Enable : bits[0]
        # read/write enable: 0 = write, 1 = read
        self.ddr4_tester.write_field("spot_rw", val)

    def reset_sequence(self):
        self.reset(True)
        time.sleep(10**(-3))
        self.reset(False)

    def maunal_read_write_test(self):
        self.write_block_test_enable_reg(False)
        self.reset_sequence()
        wr_addr_fine = 0x00
        if (self.ddr4_size == '32GB'):
            wr_addr_coarse = random.randint(0, 2**29 - 1); 
        elif (self.ddr4_size == '256GB'):
            wr_addr_coarse = random.randint(0, 2**32 - 1); 
        wr_data = random.randint(0, 2**32 - 1);   
        self.write_addr_coarse_reg(wr_addr_coarse)
        self.write_addr_fine_reg(wr_addr_fine)
        self.write_data_reg(wr_data)
        self.rw_enable(0)   # 0 = write enable
        self.rw_enable(1)   # 1 = read enable
        rd_data = self.read_data_reg()
        self.checker.check(rd_data == wr_data, f"{self.ddr4_tester_name} spot_read: addr: 0x{wr_addr_coarse:08X} data: 0x{rd_data:08X}")

    def maunal_linear_read_write_test_loop(self):
        self.write_block_test_enable_reg(False)
        self.reset_sequence()
        wr_addr_fine = 0x00
        self.write_addr_fine_reg(wr_addr_fine)
        # write data
        for addr in range(0, 2**8, 1):    # write loop
            self.write_addr_coarse_reg(addr)
            wr_data = addr + 0x70000000
            self.write_data_reg(wr_data)
            self.rw_enable(0)   # 0 = write enable
        # read / check data matches write data
        for addr in range(0, 2**8, 1):    # read loop
            self.write_addr_coarse_reg(addr) 
            wr_data = addr + 0x70000000
            self.rw_enable(1)   # 1 = read enable
            rd_data = self.read_data_reg()
            self.checker.check(rd_data == wr_data, f"{self.ddr4_tester_name} spot_read: addr: 0x{addr:08X} data: 0x{rd_data:08X}")

    def manual_random_read_write_test(self):
        self.write_block_test_enable_reg(False)
        self.reset_sequence()
        wr_addr_fine = random.randint(0, 18 - 1);  # EMIF: 576 bits / 32 bits = 18
        self.write_addr_fine_reg(wr_addr_fine)
        for idx in range(0, 2**8, 1):
            if (self.ddr4_size == '32GB'):
                wr_addr_coarse = random.randint(0, 2**29 - 1); 
            elif (self.ddr4_size == '256GB'):
                wr_addr_coarse = random.randint(0, 2**32 - 1); 
            self.write_addr_coarse_reg(wr_addr_coarse)
            wr_data = random.randint(0, 2**32 - 1);   
            self.write_data_reg(wr_data)
            self.rw_enable(0)   # 0 = write enable
            self.rw_enable(1)   # 1 = read enable
            rd_data = self.read_data_reg()
            self.checker.check(rd_data == wr_data, f"{self.ddr4_tester_name} spot_read: addr: 0x{wr_addr_coarse:08X} data: 0x{rd_data:08X}")


    def get_pattern_select_name(self, pattern):
        pattern_num = self.read_pattern_select_reg(pattern)
        if pattern_num == 0:
            pattern_str = "walking_0"
        elif pattern_num == 1:
            pattern_str = "walking_1"
        elif pattern_num == 2:
            pattern_str = "alternating_A"
        elif pattern_num == 3:
            pattern_str = "alternating_5"
        return pattern_str
   
    def update_test_status(self):
        status_reg = self.read_check_status_reg()
        if status_reg == 0xFF:
            if (self.test_status == "init"):
                self.test_status = "passed"
            elif (self.test_status == "passed"):
                self.test_status = "passed"
            else:
                self.test_status = "failed"
        else:
            self.test_status = "failed"

    def get_ddr4_max_addr(self):
        # determine the maximum read address
        if (self.ddr4_size == '32GB'):
            max_addr = 2**29 - 1     
        elif (self.ddr4_size == '256GB'):
            max_addr = 2**32 - 1     
        return max_addr

    def memory_size_tested(self, coeff):
        start_addr = self.read_start_addr_reg()
        stop_addr = self.read_stop_addr_reg()
        return round(coeff * (stop_addr - start_addr) / 2**24)  # Gigabytes

    def percent_memory_tested(self, coeff):
        if (self.ddr4_size == '32GB'):
            mem_size =  32    
        elif (self.ddr4_size == '256GB'):
            mem_size =  256    
        mem_size_tested = self.memory_size_tested(coeff)
        return round(mem_size_tested/mem_size*100, 2)


random.seed()

def ddr4_tester_config(EMIFs, regsets, checker):
    """Configure the DDR4 Tester module instances:
            module s10_emif_top_right (256GB)
            module s10_emif_bottom_right (32GB)
            module s10_emif_bottom_left (32GB)"""
    for idx in EMIFs:
        emif_list = idx.get("EMIF")
        mem_size_list = idx.get("SIZE")

    ddr4_testers = dict()
    idx = 0
    for emif in emif_list:
        ddr4_testers[f"ddr4_tester_{emif}"] = DDR4_TESTER(regsets, f"ddr4_tester_{emif}", mem_size_list[idx], checker)
        idx += 1

    for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
        # logging.info(f"DDR4 Tester dictionary: key = {ddr4_tester_name}, value = {ddr4_tester}, size = {ddr4_tester.ddr4_size}")
        ddr4_tester.check_ver_id_reg()
        ddr4_tester.reset_sequence()

    return [ddr4_testers]


def ddr4_manual_random_read_write_test(EMIFs, ddr4_testers, runtime):
    """
    DDR4 Tester manual random data / address read/write test.
    Enables the FPGA DDR4 Tester module manual read/write test
    for the specified address and data.
    """
    for idx in EMIFs:
        emif_list = idx.get("EMIF")

    logging.info(f"DDR4 Tester block pattern test.")
    start = time.time()
    with tqdm.tqdm(desc=f"DDR4 random data/addr loop test", total=runtime*len(emif_list)+0.075, unit="Seconds", unit_scale=False, initial=0) as pbar:
        for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
            time_last = time_current = time.time()
            max_addr = ddr4_tester.get_ddr4_max_addr()
            ddr4_tester.write_block_test_enable_reg(False)
            ddr4_tester.reset_sequence()
            wr_addr_fine = 0x00  # EMIF: 576 bits / 32 bits = 18
            ddr4_tester.write_addr_fine_reg(wr_addr_fine)
            time_current = time.time()
            while ((time_current - time_last) <= runtime):
                wr_addr_coarse = random.randint(0, max_addr); 
                ddr4_tester.write_addr_coarse_reg(wr_addr_coarse)
                wr_data = random.randint(0, 2**32 - 1);   
                ddr4_tester.write_data_reg(wr_data)
                ddr4_tester.rw_enable(0)   # 0 = write enable
                ddr4_tester.rw_enable(1)   # 1 = read enable
                rd_data = ddr4_tester.read_data_reg()
                ddr4_tester.checker.check_quiet(rd_data == wr_data, f"message holder")
                time_current = time.time()
            pbar.update(time_current-time_last)
        pbar.close
    end = time.time()
    logging.info(f"DDR4 Tester manual random data test finished in {end-start:1.1f} seconds.")


def ddr4_tester_manual_rw_check(ddr4_testers):
    """
    DDR4 Tester manual read/write test functions.
    Enables the FPGA DDR4 Tester module manual read/write test
    for the specified address and data.
    """
    for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
        ddr4_tester.maunal_read_write_test()
        # ddr4_tester.maunal_linear_read_write_test_loop()
        # ddr4_tester.manual_random_read_write_test()

def length(addr):
    start_word_addr = 0
    return (addr - start_word_addr)


def ddr4_tester_block_pattern_rw_check_tqdm(EMIFs, ddr4_testers, pattern, current_time):
    """
    Block pattern test function to check the DDR4 memory using the specified 
    word pattern. The DDR4 Tester verifies the entire DDR4 memory space by 
    writing a 8 x 72-bit pattern to the EMIF and reads the memory to check it 
    matches the generated block test pattern.
    """

    # 0x01000000    # 1GB
    # 0x02000000    # 2GB
    # 0x04000000    # 4GB
    # 0x08000000    # 8GB
    # 0x10000000    # 16GB
    # 0x1FFFFFFF    # 32GB
    # 0x20000000    # 32GB
    # 0x40000000    # 64GB
    # 0x80000000    # 128GB
    # 0xFFFFFFFF    # 256GB

    # # full 32GB memory test, takes ~46s
    # STEP_CNT = 1
    # start_addr_base = 0x00000000
    # stop_addr_base  = 0x10000000    # 16GB
    # # stop_addr_base  = 0x1FFFFFFF    # 32GB
    # step_size = 0x00000001         # every address

    # # 16GB of 32GB memory test, takes ~25
    # STEP_CNT = 4
    # start_addr_base = 0x00000000
    # stop_addr_base  = 0x04000000    # 4GB
    # step_size = 0x08000000    # 8GB

    # 16GB of 32GB memory test, takes ~25
    # STEP_CNT = 8
    # start_addr_base = 0x00000000
    # stop_addr_base  = 0x02000000    # 2GB
    # step_size = 0x04000000    # 4GB

    # 16GB of 32GB memory test, takes ~26
    STEP_CNT = 16
    start_addr_base = 0x00000000
    stop_addr_base  = 0x01000000    # 1GB
    step_size = 0x02000000    # 2GB

    COEFF_256 = int(256/32)
    block_size = stop_addr_base - start_addr_base

    start_addr = start_addr_base
    stop_addr = stop_addr_base
    rd_addr_total = (stop_addr - start_addr) * STEP_CNT
    logging.info(f"step_size: 0x{step_size:08X}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}, rd_addr_total: 0x{rd_addr_total:08X}")

    logging.info(f"DDR4 Tester block pattern test.")
    start = time.time()

    with tqdm.tqdm(desc="DDR4 Block Test", total=rd_addr_total, unit="Bytes", unit_scale=False, initial=0) as pbar:
        for lc in range (0, STEP_CNT, 1):
            start_addr = start_addr_base + step_size*lc
            stop_addr = stop_addr_base + step_size*lc
            logging.debug(f"loop cnt: {lc}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}")
            for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
                if ddr4_tester.ddr4_size == '256GB':
                    start_addr = COEFF_256 * start_addr
                    stop_addr = start_addr + block_size
                    logging.debug(f"loop cnt: {lc}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}")
                ddr4_tester.configure_block_test(pattern, start_addr, stop_addr)
                if f"{ddr4_tester.ddr4_tester_name}" == "ddr4_tester_TR":
                    last = 0
                    current = length(ddr4_tester.read_current_rd_addr_reg())
                    pbar.update(current - last)
            for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
                while ddr4_tester.read_check_done_reg() != True:
                    if f"{ddr4_tester.ddr4_tester_name}" == "ddr4_tester_TR":
                        last = current
                        current = length(ddr4_tester.read_current_rd_addr_reg())
                        pbar.update(current - last)
                        time.sleep(0.5)
                if f"{ddr4_tester.ddr4_tester_name}" == "ddr4_tester_TR":
                    last = current
                    current = length(ddr4_tester.read_current_rd_addr_reg())
                    pbar.update(current - last)
                ddr4_tester.check_block_pattern_test_status()
                ddr4_tester.update_test_status()
                ddr4_tester.write_block_test_enable_reg(False)            
    end = time.time()
    logging.info(f"DDR4 Tester block test finished in {end-start:1.1f} seconds.")

    logging.info(f"DDR4 Tester Block Test Summary")

    for idx in EMIFs:
        board = idx.get("board")
        emif_list = idx.get("EMIF")

    influx_csv_writer = bist_utils.influx_csv('bist.csv')
    data_type = ['measurement','tag','string','double', 'double','string','string','long','long','dateTime:RFC3339']
    influx_csv_writer.write_datatype(data_type)

    # Display the DDR4 Tester Block Test BIST Status
    header_col = [
        "Register",
        "EMIF",
        "Memory Size",
        "Memory Checked(GB)",
        "Memory Checked(%)",
        "Test Pattern",
        "Test Status",
        "Error Count",
        "Error Address",
    ]
    table = BeautifulTable(maxwidth=200, precision=32)
    table.columns.header = header_col
    influx_csv_writer.write_header(header_col)
    idx = 0
    for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
        data_row = []
        data_row = (
            data_row
            + [board]
            + [f"EMIF_{emif_list[idx]}"]
            + [ddr4_tester.ddr4_size]
            + [f"{ddr4_tester.memory_size_tested(STEP_CNT)}"]
            + [f"{ddr4_tester.percent_memory_tested(STEP_CNT)}"]
            + [ddr4_tester.get_pattern_select_name(pattern)]
            + [ddr4_tester.test_status]
            + [ddr4_tester.read_error_count_reg()]
            + [ddr4_tester.read_error_addr_reg()]
            )
        table.rows.append(data_row)
        influx_csv_writer.write_csv(data_row, current_time)
        idx += 1
    logging.info(table)


def ddr4_tester_block_pattern_rw_check(EMIFs, ddr4_testers, pattern, current_time):
    """
    Block pattern test function to check the DDR4 memory using the specified 
    word pattern. The DDR4 Tester verifies the entire DDR4 memory space by 
    writing a 8 x 72-bit pattern to the EMIF and reads the memory to check it 
    matches the generated block test pattern.
    """

    # # 16GB of 32GB/256GB memory test, takes ~25 s
    # STEP_CNT = 4
    # start_addr_base = 0x00000000
    # stop_addr_base  = 0x04000000    # 4GB
    # step_size = 0x08000000    # 8GB

    # # 16GB of 32GB/256GB memory test, takes ~27
    # STEP_CNT = 8
    # start_addr_base = 0x00000000
    # stop_addr_base  = 0x02000000    # 2GB
    # step_size = 0x04000000    # 4GB

    # 16GB of 32GB/256GB memory test, takes ~29 s
    STEP_CNT = 16
    start_addr_base = 0x00000000
    stop_addr_base  = 0x01000000    # 1GB
    step_size = 0x02000000    # 2GB

    COEFF_256 = int(256/32)
    block_size = stop_addr_base - start_addr_base

    start_addr = start_addr_base
    stop_addr = stop_addr_base
    rd_addr_total = (stop_addr - start_addr) * STEP_CNT
    logging.info(f"step_size: 0x{step_size:08X}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}, rd_addr_total: 0x{rd_addr_total:08X}")

    logging.info(f"DDR4 Tester block pattern test.")
    start = time.time()
    for lc in range (0, STEP_CNT, 1):
        start_addr = start_addr_base + step_size*lc
        stop_addr = stop_addr_base + step_size*lc
        logging.debug(f"loop cnt: {lc}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}")
        for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
            if ddr4_tester.ddr4_size == '256GB':
                start_addr = COEFF_256 * start_addr
                stop_addr = start_addr + block_size
                logging.debug(f"loop cnt: {lc}, start_addr: 0x{start_addr:08X}, stop_addr: 0x{stop_addr:08X}")
            ddr4_tester.configure_block_test(pattern, start_addr, stop_addr)
        for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
            while ddr4_tester.read_check_done_reg() != True:
                    time.sleep(0.5)
            ddr4_tester.check_block_pattern_test_status()
            ddr4_tester.update_test_status()
            ddr4_tester.write_block_test_enable_reg(False)            
    end = time.time()
    logging.info(f"DDR4 Tester block test finished in {end-start:1.1f} seconds.")

    logging.info(f"DDR4 Tester Block Test Summary")
    for idx in EMIFs:
        board = idx.get("board")
        emif_list = idx.get("EMIF")

    influx_csv_writer = bist_utils.influx_csv('bist.csv')
    data_type = ['measurement','tag','string','double', 'double','string','string','long','long','dateTime:RFC3339']
    influx_csv_writer.write_datatype(data_type)

    # Display the DDR4 Tester Block Test BIST Status
    header_col = [
        "Register",
        "EMIF",
        "Memory Size",
        "Memory Checked(GB)",
        "Memory Checked(%)",
        "Test Pattern",
        "Test Status",
        "Error Count",
        "Error Address",
    ]
    table = BeautifulTable(maxwidth=200, precision=32)
    table.columns.header = header_col
    influx_csv_writer.write_header(header_col)
    idx = 0
    for ddr4_tester_name, ddr4_tester in ddr4_testers.items():
        data_row = ['ddr_test']
        data_row = (
            data_row
            + [f"EMIF_{emif_list[idx]}"]
            + [ddr4_tester.ddr4_size]
            + [f"{ddr4_tester.memory_size_tested(STEP_CNT)}"]
            + [f"{ddr4_tester.percent_memory_tested(STEP_CNT)}"]
            + [ddr4_tester.get_pattern_select_name(pattern)]
            + [ddr4_tester.test_status]
            + [ddr4_tester.read_error_count_reg()]
            + [ddr4_tester.read_error_addr_reg()]
            )
        table.rows.append(data_row)
        influx_csv_writer.write_csv(data_row, current_time)
        idx += 1
    logging.info(table)


def main(EMIFs, pattern, runtime, regsets, current_time):
    # bist_utils.Date().log_timestamp()
    checker = bist_utils.Checker()
    logging.info(f"#---------------------------------------------------------")
    logging.info(f"Talon-DX FPGA BIST testcase: DDR4")
    [ddr4_testers] = ddr4_tester_config(EMIFs, regsets, checker)
    ddr4_tester_manual_rw_check(ddr4_testers)
    # ddr4_manual_random_read_write_test(EMIFs, ddr4_testers, runtime)
    ddr4_tester_block_pattern_rw_check_tqdm(EMIFs, ddr4_testers, pattern, current_time)
    # ddr4_tester_block_pattern_rw_check(EMIFs, ddr4_testers, pattern, current_time)
    checker.report_log(f"DDR4 Tester test results")
    return checker



if __name__ == "__main__":
    logging.info("tdc_base_bist_ddr4: __main__")
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
        testcase = "DDR4_Walking_1_Pattern",
        DDR4_runtime = 5.0,          # test time in seconds
        # DDR4 Tester module
        DDR4_EMIFs = [
        {
            'board': "talon", 
            "EMIF": ['TR', 'BL', 'BR'],
            "SIZE": ['256GB', '32GB', '32GB'],
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
        logging.info("Arguments loaded from defaults in script")

    testcase = args.get('testcase')
    assert ((testcase == "DDR4_Walking_0_Pattern") or \
            (testcase == "DDR4_Walking_1_Pattern") or \
            (testcase == "DDR4_Alternating_A_Pattern") or \
            (testcase == "DDR4_Alternating_5_Pattern")), \
            f"DDR4 BIST: {testcase} testcase not found"
    runtime = args.get('DDR4_runtime')
    EMIFs = args.get('DDR4_EMIFs') 

    #-------------------------------------------------------------------------
    # FPGA module BIST test: 
    #-------------------------------------------------------------------------
    # DDR4 Tester testcases: 72-bit test patterns
    if testcase == "DDR4_Walking_0_Pattern":            # 0xFFFFFFFFFFFFFFFFFE
        pattern = 0
    elif testcase == "DDR4_Walking_1_Pattern":          # 0x000000000000000001
        pattern = 1
    elif testcase == "DDR4_Alternating_A_Pattern":      # 0xAAAAAAAAAAAAAAAAAA
        pattern = 2
    elif testcase == "DDR4_Alternating_5_Pattern":      # 0x555555555555555555
        pattern = 3
    else:
        logging.error(f"Invalid testcase {testcase}!")

    checker = main(EMIFs, pattern, runtime, regsets)    