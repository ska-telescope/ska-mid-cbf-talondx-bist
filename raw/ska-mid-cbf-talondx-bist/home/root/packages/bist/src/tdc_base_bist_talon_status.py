#!/usr/bin/python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1283 Report Talon Status parameters as part of BIST script.
#
# File Name: tdc_base_bist_talon_status.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script - Talon Status.
#
# BIST script for accessing FPGA registers. Note register_access.py is 
# imported to access the FPGA registers. The script is run directly on the 
# Talon board in Python stand-alone mode. 
# Test status is output to the Python logger utility.
#
# Date: 10 FEB 2023, developed during PI17
#
# args: <filename>.json and <filename>.ipmap files
#
# Run on talon board as follows:
# root@talon:~# 
#     python3 tdc_base_bist_talon_status.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#
# Talon status checks:
#   1. Faults
#   2. Clocks (PLL locked status, clock frequency)
#   3. External Memory Interface (EMIF)
#   4. 100Gb Ethernet
#   5. SLIM
#  
#-----------------------------------------------------------------------------
import sys
from beautifultable import BeautifulTable
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

import bist_utils

class TS_Fault:
    def __init__(self, talon_status, name, checker) -> None:
        self.ts_fault = talon_status
        self.ts_name = name
        self.checker = checker
        self.ts_reg = []

    def check_talon_fault_status(self):

        # System Clock Fault: bits[0]
        # Indicates a fault with the 125MHz source clock being not operational 
        # or not at the expected frequency. Further internal clocks are derived
        # from this clock and would imply no other core functions are working.
        # ts_reg = self.ts_fault.read_field("system_clk_fault")
        # self.checker.check(ts_reg == False, f"{self.ts_name} system_clk_fault: {ts_reg}")
        ts_reg = self.ts_fault.read_field("system_clk_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} system_clk_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # PLL Locked Fault: bits[0]
        # Returns the vcc_base_iopll PLL locked status signal. 
        # This PLL sources the 125MHz and 100MHz clocks. Indicates a problem 
        # with source 125MHz reference clock.
        ts_reg = self.ts_fault.read_field("iopll_locked_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} iopll_locked_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # FS PLL Locked Fault: bits[0]
        # Returns the fs_iopll PLL locked status signal. This PLL sources the
        # 450MHz clock. Indicates a problem with source 125MHz reference clock.
        ts_reg = self.ts_fault.read_field("fs_iopll_locked_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} fs_iopll_locked_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # Comms PLL Locked Fault: bits[0]
        # Returns the comms_iopll PLL locked status signal. This PLL sources the
        # 400MHz clock. Indicates a problem with source 125MHz reference clock.
        ts_reg = self.ts_fault.read_field("comms_iopll_locked_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} comms_iopll_locked_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # EMIF Bottom Left Fault: bits[0]
        # Returns the summary status of the bottom left EMIF. A high indicates
        # a fault with calibration, PLL lock or clock frequency.
        ts_reg = self.ts_fault.read_field("emif_bl_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} emif_bl_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # EMIF Bottom Right Fault: bits[0]
        # Returns the summary status of the bottom right EMIF. A high indicates
        # a fault with calibration, PLL lock or clock frequency.
        ts_reg = self.ts_fault.read_field("emif_br_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} emif_br_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # EMIF Top Right Fault: bits[0]
        # Returns the summary status of the top right EMIF. A high indicates
        # a fault with calibration, PLL lock or clock frequency.
        ts_reg = self.ts_fault.read_field("emif_tr_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} emif_tr_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # 100GbE 0 PLL Fault: bits[0]
        # Returns the summary status of the first 100GbE transceiver's PLLs.
        # A high indicates a fault with one of the two PLLs.
        ts_reg = self.ts_fault.read_field("e100g_0_pll_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} e100g_0_pll_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # 100GbE 1 PLL Fault: bits[0]
        # Returns the summary status of the second 100GbE transceiver's PLLs.
        # A high indicates a fault with one of the two PLLs.
        ts_reg = self.ts_fault.read_field("e100g_1_pll_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} e100g_1_pll_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # SLIM PLL Fault: bits[0]
        # Returns the summary status of the SLIM PPLs. A high indicates a fault
        # with at least one of the SLIMs.
        ts_reg = self.ts_fault.read_field("slim_pll_fault")
        self.checker.check(ts_reg == False, f"{self.ts_name} slim_pll_fault: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # Non Zero Pattern 0xC...: bits[5:0]
        # A non-zero 0xC fixed bit pattern to indicate successful register 
        # access confirming the HPS and DeTrI interface clocks are operational.
        ts_reg = self.ts_fault.read_field("non_zero")
        logging.debug(f"Talon Status non_zero: 0x{ts_reg:02X}")
        self.checker.check(ts_reg >= (2**5+2**4), f"{self.ts_name} non_zero: 0x{ts_reg:02X}")
        self.ts_reg = self.ts_reg + [f"0x{ts_reg:02X}"]

    def talon_fault_status_table(self):
        logging.info(f"Talon Fault Status Summary")
        header_col = [ 
            "SysClk ",
            "PLL",
            "FS PLL",
            "COMMS PLL",
            "EMIF BL",
            "EMIF BR",
            "EMIF TR",
            "ETH0 PLL",
            "ETH1 PLL",
            "SLIM PLLs",
            "Non Zero",
            ]
        table = BeautifulTable(maxwidth=200, precision=32)
        table.columns.header = header_col
        data_row = []
        for idx in range(0,len(self.ts_reg),1):
            data_row = data_row + [f"{self.ts_reg[idx]}"]
        table.rows.append(data_row)
        logging.info(table)

def talon_fault_status(talon_status,checker):
    fault = TS_Fault(talon_status, f"talon_fault_status", checker)
    fault.check_talon_fault_status()
    fault.talon_fault_status_table()


class TS_Clock:
    def __init__(self, talon_status, name, checker) -> None:
        self.ts_clock = talon_status
        self.ts_name = name
        self.checker = checker
        self.ts_reg = []

    def check_talon_clock_status(self):

        # Base Clock Frequency: bits[31:0]
        # Frequency counter for the 125 MHz clock. The value returned should be
        # 125,000,000 ± 70 ppm (± 8750 Hz). This clock is the base for other 
        # derived system clocks. Updated every second.
        ts_reg = self.ts_clock.read_field("base_clock_frequency")
        self.checker.check(
            (ts_reg >= (1.25000000*(10**8) - 8750) and
             ts_reg <= (1.25000000*(10**8) + 8750)),
            f"{self.ts_name} base_clock_frequency: {ts_reg/10**6} MHz"
            )
        self.ts_reg = self.ts_reg + [ts_reg/10**6]

        # EMIF Bottom Left Clock Frequency: bits[31:0]
        # Frequency counter for the EMIF interface clock. The value returned
        # should be 333,333,333 ± 70 ppm (± 23,333 Hz). Updated every second.
        ts_reg = self.ts_clock.read_field("emif_bl_clock_frequency")
        self.checker.check(
            ((ts_reg >= (3.33333333*(10**8) - 2.3333*(10**4))) and
             (ts_reg <= (3.33333333*(10**8) + 2.3333*(10**4)))),
            f"{self.ts_name} emif_bl_clock_frequency: {ts_reg/10**6} MHz"
            )
        self.ts_reg = self.ts_reg + [ts_reg/10**6]

        # EMIF Bottom Right Clock Frequency: bits[31:0]
        # Frequency counter for the EMIF interface clock. The value returned
        # should be 333,333,333 ± 70 ppm (± 23,333 Hz). Updated every second.
        ts_reg = self.ts_clock.read_field("emif_br_clock_frequency")
        self.checker.check(
            ((ts_reg >= (3.33333333*(10**8) - 2.3333*(10**4))) and
             (ts_reg <= (3.33333333*(10**8) + 2.3333*(10**4)))),
            f"{self.ts_name} emif_br_clock_frequency: {ts_reg/10**6} MHz"
            )
        self.ts_reg = self.ts_reg + [ts_reg/10**6]

        # EMIF Top Right Clock Frequency: bits[31:0]
        # Frequency counter for the EMIF interface clock. The value returned
        # should be 333,333,333 ± 70 ppm (± 23,333 Hz). Updated every second.
        ts_reg = self.ts_clock.read_field("emif_tr_clock_frequency")
        self.checker.check(
            ((ts_reg >= (3.33333333*(10**8) - 2.3333*(10**4))) and
             (ts_reg <= (3.33333333*(10**8) + 2.3333*(10**4)))),
            f"{self.ts_name} emif_tr_clock_frequency: {ts_reg/10**6} MHz"
            )
        self.ts_reg = self.ts_reg + [ts_reg/10**6]

        # PLL Locked Transition: bits[0]
        # Cleared by writing a '1' to this status bit.
        self.ts_clock.write_field("iopll_locked_trn", 1)
        ts_reg = self.ts_clock.read_field("iopll_locked_trn")
        self.checker.check(ts_reg == False, f"{self.ts_name} iopll_locked_trn: {ts_reg}")

        # PLL Locked: bits[0]
        # Returns the vcc_base_iopll PLL locked status signal. This PLL sources
        # the 125MHz and 100MHz clocks. Indicates a problem with source 125MHz
        # reference clock. Should normally be True.
        ts_reg = self.ts_clock.read_field("iopll_locked")
        self.checker.check(ts_reg == True, f"{self.ts_name} iopll_locked: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # FS PLL Locked Transition: bits[0]
        # Cleared by writing a '1' to this status bit.
        self.ts_clock.write_field("fs_iopll_locked_trn", 1)
        ts_reg = self.ts_clock.read_field("fs_iopll_locked_trn")
        self.checker.check(ts_reg == False, f"{self.ts_name} fs_iopll_locked_trn: {ts_reg}")

        # FS PLL Locked: bits[0]
        # Returns the fs_iopll PLL locked status signal. This PLL sources the
        # 450MHz clock. Indicates a problem with source 125MHz reference clock.
        # Should normally be True.
        ts_reg = self.ts_clock.read_field("fs_iopll_locked")
        self.checker.check(ts_reg == True, f"{self.ts_name} fs_iopll_locked: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # Comms PLL Locked Transition: bits[0]
        # Cleared by writing a '1' to this status bit.
        self.ts_clock.write_field("comms_iopll_locked_trn", 1)
        ts_reg = self.ts_clock.read_field("comms_iopll_locked_trn")
        self.checker.check(ts_reg == False, f"{self.ts_name} comms_iopll_locked_trn: {ts_reg}")

        # Comms PLL Locked: bits[0]
        # Returns the comms_iopll PLL locked status signal. This PLL sources 
        # the 400MHz clock. Indicates a problem with source 125MHz reference
        # clock. Should normally be True.
        ts_reg = self.ts_clock.read_field("comms_iopll_locked")
        self.checker.check(ts_reg == True, f"{self.ts_name} comms_iopll_locked: {ts_reg}")
        self.ts_reg = self.ts_reg + [ts_reg]

    def talon_clock_status_table(self):
        logging.info(f"Talon Clock Status Summary")
        header_col = [ 
            "Base Clk (MHz)",
            "EMIF BL Clk (MHz)",
            "EMIF BR Clk (MHz)",
            "EMIF TR Clk (MHz)",
            "PLL Locked",
            "FS PLL Locked",
            "Comms PLL Locked",
            ]
        table = BeautifulTable(maxwidth=200, precision=32)
        table.columns.header = header_col
        data_row = []
        for idx in range(0,len(self.ts_reg),1):
            data_row = data_row + [f"{self.ts_reg[idx]}"]
        table.rows.append(data_row)
        logging.info(table)

def talon_clock_status(talon_status, checker):
    clock = TS_Clock(talon_status, f"talon_clock_status", checker)
    clock.check_talon_clock_status()
    clock.talon_clock_status_table()


class TS_EMIF:
    def __init__(self, talon_status, name, checker) -> None:
        self.ts_emif = talon_status
        self.ts_name = name
        self.checker = checker
        self.repeat = 3
        self.ts_reg = [[] for emif in range(self.repeat)]

    def emif_reset(self, emif_no, val):
            # EMIF Reset: bits[0]
            # Asserts the local_reset_req signal to the EMIF to restart 
            # calibration. SW must write a '1' followed by a '0' to restart calibration.
            self.ts_emif.write_field("emif_reset", emif_no, val)
    def check_talon_emif_status(self):
        for idx in range(0,self.repeat,1):

            # PLL Locked Transition: bits[0]
            # Indicates a transition of the pll_locked signal from the EMIF PLL.
            # Cleared by writing a '1' to this status bit.
            self.ts_emif.write_field("emif_pll_locked_trn", 1, idx)
            ts_reg = self.ts_emif.read_field("emif_pll_locked_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_pll_locked_trn: {ts_reg}")

            # PLL Locked: bits[0]
            # Returns the state of the pll_locked signal from the EMIF PLL. 
            # Failure to lock would indicate a problem with the reference clock
            # missing or being unstable. Should normally be True.
            # ts_reg = self.ts_emif.read_field("emif_pll_locked[0]")
            ts_reg = self.ts_emif.read_field("emif_pll_locked", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} emif{idx}: emif_pll_locked: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]
    
            # Local Reset Done Transition: bits[0]
            # Indicates a transition of the local_reset_done signal from the EMIF.
            # Cleared by writing a '1' to this status bit.
            self.ts_emif.write_field("emif_local_reset_done_trn", 1, idx)
            ts_reg = self.ts_emif.read_field("emif_local_reset_done_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_local_reset_done_trn: {ts_reg}")

            # Local Reset Done: bits[0]
            # Returns the state of the local_reset_done signal from the EMIF.
            # Should normally be True.
            ts_reg = self.ts_emif.read_field("emif_local_reset_done", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} emif{idx}: emif_local_reset_done: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # Local Cal Success Transition: bits[0]
            # Indicates a transition of the local_cal_success signal from the EMIF.
            # Cleared by writing a '1' to this status bit.
            self.ts_emif.write_field("emif_local_cal_success_trn", 1, idx)
            ts_reg = self.ts_emif.read_field("emif_local_cal_success_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_local_cal_success_trn: {ts_reg}")

            # Local Cal Success: bits[0]
            # Returns the state of the local_cal_success signal from the EMIF.
            # Should normally be True.
            ts_reg = self.ts_emif.read_field("emif_local_cal_success", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} emif{idx}: emif_local_cal_success: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # Local Cal Fail Transition: bits[0]
            # Indicates a transition of local_cal_fail signal from the EMIF.
            # Cleared by writing a '1' to this status bit.
            self.ts_emif.write_field("emif_local_cal_fail_trn", 1, idx)
            ts_reg = self.ts_emif.read_field("emif_local_cal_fail_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_local_cal_fail_trn: {ts_reg}")

            # Local Cal Fail: bits[0]
            # Returns the state of the local_cal_fail signal from the EMIF. 
            # Indicates a fault with the interface to the DDR4 DIMM module. 
            # Should normally be False.
            ts_reg = self.ts_emif.read_field("emif_local_cal_fail", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_local_cal_fail: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # AMM Ready Transition: bits[0]
            # Indicates a transition of the amm_ready_0 signal from the EMIF.
            # Cleared by writing a '1' to this status bit.
            self.ts_emif.write_field("emif_amm_ready_trn", 1, idx)
            ts_reg = self.ts_emif.read_field("emif_amm_ready_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} emif{idx}: emif_amm_ready_trn: {ts_reg}")

            # AMM Ready: bits[0]
            # Returns the state of the amm_ready_0 signal from the EMIF. 
            # Indicates that the Avalon memory interface is ready to receive
            # access requests. Should normally be True.
            ts_reg = self.ts_emif.read_field("emif_amm_ready", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} emif{idx}: emif_amm_ready: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

    def talon_emif_status_table(self):
        logging.info(f"Talon EMIF Status Summary")
        header_col = [ 
            " ",
            "PLL Locked",
            "Reset Done",
            "Cal Success",
            "Cal Fail",
            "AMM Ready",
            ]
        table = BeautifulTable(maxwidth=200, precision=32)
        table.columns.header = header_col
        for emif in range(0,self.repeat,1):
            data_row = []
            data_row = data_row + [f"EMIF{emif}"]
            for idx in range(0,len(self.ts_reg[emif]),1):
                data_row = data_row + [f"{self.ts_reg[emif][idx]}"]
            table.rows.append(data_row)
        logging.info(table)


def talon_emif_status(talon_status, checker):
    emif = TS_EMIF(talon_status, f"talon_emif_status", checker)
    emif.check_talon_emif_status()
    emif.talon_emif_status_table()


class TS_E100G:
    def __init__(self, talon_status, name, checker) -> None:
        self.ts_e100g = talon_status
        self.ts_name = name
        self.checker = checker
        self.repeat = 2
        self.ts_reg = [[] for e100g in range(self.repeat)]

    def check_talon_e100g_status(self):
        for idx in range(0,self.repeat,1):

            # 100GbE Main ATX PLL Locked Transition: bits[0]
            # Indicates a transition of the pll_locked signal from the main ATX PLL.
            # Cleared by writing a '1' to this status bit.
            self.ts_e100g.write_field("e100g_main_pll_locked_trn", 1, idx)
            ts_reg = self.ts_e100g.read_field("e100g_main_pll_locked_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_main_pll_locked_trn: {ts_reg}")

            # 100GbE Main ATX PLL Locked: bits[0]
            # Returns the state of the pll_locked signal from the main ATX PLL.
            # Failure to lock would indicate a missing or unstable reference
            # clock. Should normally be True.
            ts_reg = self.ts_e100g.read_field("e100g_main_pll_locked", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} eth{idx}: e100g_main_pll_locked: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # 100GbE Main ATX PLL Calibration Busy Transition: bits[0]
            # Indicates a transition of the pll_cal_busy signal from the main ATX PLL.
            # Cleared by writing a '1' to this status bit.
            self.ts_e100g.write_field("e100g_main_pll_cal_busy_trn", 1, idx)
            ts_reg = self.ts_e100g.read_field("e100g_main_pll_cal_busy_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_main_pll_cal_busy_trn: {ts_reg}")

            # 100GbE Main ATX PLL Calibration Busy: bits[0]
            # Returns the state of the pll_cal_busy signal from the main ATX PLL. 
            # Failure to calibrate would indicate an unstable reference clock. 
            # Should normally be False.
            ts_reg = self.ts_e100g.read_field("e100g_main_pll_cal_busy", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_main_pll_cal_busy: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # 100GbE Buffer ATX PLL Locked Transition: bits[0]
            # Indicates a transition of the pll_locked signal from the buffer ATX PLL.
            # Cleared by writing a '1' to this status bit.
            self.ts_e100g.write_field("e100g_buffer_pll_locked_trn", 1, idx)
            ts_reg = self.ts_e100g.read_field("e100g_buffer_pll_locked_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_buffer_pll_locked_trn: {ts_reg}")

            # 100GbE Buffer ATX PLL Locked: bits[0]
            # Returns the state of the pll_locked signal from the buffer ATX PLL. 
            # Failure to lock would indicate a missing or unstable reference clock. 
            # Should normally be True.
            ts_reg = self.ts_e100g.read_field("e100g_buffer_pll_locked", idx)
            self.checker.check(ts_reg == True, f"{self.ts_name} eth{idx}: e100g_buffer_pll_locked: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # 100GbE Buffer ATX PLL Calibration Busy Transition: bits[0]
            # Indicates a transition of the pll_cal_busy signal from the buffer ATX PLL.
            # Cleared by writing a '1' to this status bit.
            self.ts_e100g.write_field("e100g_buffer_pll_cal_busy_trn", 1, idx)
            ts_reg = self.ts_e100g.read_field("e100g_buffer_pll_cal_busy_trn", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_buffer_pll_cal_busy_trn: {ts_reg}")
            self.ts_reg[idx] = self.ts_reg[idx] + [ts_reg]

            # 100GbE Buffer ATX PLL Calibration Busy: bits[0]
            # Returns the state of the pll_cal_busy signal from the buffer ATX PLL. 
            # Failure to calibrate would indicate an unstable reference clock. 
            # Should normally be False.
            ts_reg = self.ts_e100g.read_field("e100g_buffer_pll_cal_busy", idx)
            self.checker.check(ts_reg == False, f"{self.ts_name} eth{idx}: e100g_buffer_pll_cal_busy: {ts_reg}")

    def talon_e100g_status_table(self):
        logging.info(f"Talon E100G Status Summary")
        header_col = [ 
            " ",
            "Main PLL Locked",
            "Main PLL Cal Busy",
            "Buffer PLL Locked",
            "Buffer PLL Cal Busy",
            ]
        table = BeautifulTable(maxwidth=200, precision=32)
        table.columns.header = header_col
        for emif in range(0,self.repeat,1):
            data_row = []
            data_row = data_row + [f"E100G{emif}"]
            for idx in range(0,len(self.ts_reg[emif]),1):
                data_row = data_row + [f"{self.ts_reg[emif][idx]}"]
            table.rows.append(data_row)
        logging.info(table)

def talon_e100g_status(talon_status, checker):
    e100g = TS_E100G(talon_status, f"talon_e100g_status", checker)
    e100g.check_talon_e100g_status()
    e100g.talon_e100g_status_table()


class TS_SLIM:
    def __init__(self, talon_status, name, checker) -> None:
        self.ts_slim = talon_status
        self.ts_name = name
        self.checker = checker
        self.ts_reg = []

    def check_talon_slim_status(self):

        # SLIM Is Present (LSW): bits[31:0]
        # High when the SLIM is present in the FPGA build. 
        # Uses to mask the following corresponding SLIM status registers.
        ts_slim_mask_lsw = self.ts_slim.read_field("slim_is_present_lsw")
        logging.info(f"{self.ts_name} slim_is_present_lsw: 0x{ts_slim_mask_lsw:08X}")
        self.ts_reg = self.ts_reg + [ts_slim_mask_lsw]

        # SLIM Is Present (MSW): bits[23:0]
        # High when the SLIM is present in the FPGA build. 
        # Uses to mask the following corresponding SLIM status registers.
        ts_slim_mask_msw = self.ts_slim.read_field("slim_is_present_msw")
        logging.info(f"{self.ts_name} slim_is_present_msw: 0x{ts_slim_mask_msw:06X}")
        self.ts_reg = self.ts_reg + [ts_slim_mask_msw]

        #---------------------------------------------------------------------
        # Stratix 10 GTX H-Tile ATXPLL-to-MBO XCVR mapping:
        # MBO[1:4]
        # Bank0 ATXPLL1 -> 6 PMA Channels
        # Bank2 ATXPLL0 -> 6 PMA Channels
        # 48 Channels / 6 Channels per ATXPLL = 8 ATXPLLs
        # MBO[5]
        # TL Bank3 ATXPLL1 -> 4 PMA Channels
        # BL Bank3 ATXPLL1 -> 4 PMA Channels
        # 8 Channels / 4 Channels per ATXPLL = 2 ATXPLLs
        #---------------------------------------------------------------------
        # SLIM Top Left PLL Locked Transition (LSW): bits[31:0]
        # Indicates a transition of the SLIM PLL pll_locked signals.
        # Cleared by writing a '1' to this status bit.
        self.ts_slim.write_field("slim_pll_locked_status_trn_lsw", ts_slim_mask_lsw)
        ts_reg = self.ts_slim.read_field("slim_pll_locked_status_trn_lsw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_locked_status_trn_lsw: 0x{ts_reg:08X}")

        # SLIM PLL Locked Status (LSW): bits[31:0]
        # Status of the SLIM PLL pll_locked signals. 
        # Should normally be all True.
        ts_reg = self.ts_slim.read_field("slim_pll_locked_status_lsw")
        self.checker.check(ts_reg == ts_slim_mask_lsw, f"{self.ts_name} slim_pll_locked_status_lsw: 0x{ts_reg:08X}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # SLIM Top Left PLL Locked Transition (MSW): bits[23:0]
        # Indicates a transition of the SLIM PLL pll_locked signals.
        # Cleared by writing a '1' to this status bit.
        self.ts_slim.write_field("slim_pll_locked_status_trn_msw", ts_slim_mask_msw)
        ts_reg = self.ts_slim.read_field("slim_pll_locked_status_trn_msw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_locked_status_trn_msw: 0x{ts_reg:06X}")

        # SLIM PLL Locked Status (MSW): bits[23:0]
        # Status of the SLIM PLL pll_locked signals. 
        # Should normally be all True.
        ts_reg = self.ts_slim.read_field("slim_pll_locked_status_msw")
        self.checker.check(ts_reg == ts_slim_mask_msw, f"{self.ts_name} slim_pll_locked_status_msw: 0x{ts_reg:06X}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # SLIM PLL Calibration Busy Transition (LSW): bits[31:0]
        # Indicates a transition of the 8 SLIM PLL pll_cal_busysignals.
        # Cleared by writing a '1' to this status bit.
        self.ts_slim.write_field("slim_pll_cal_busy_status_trn_lsw", ts_slim_mask_lsw)
        ts_reg = self.ts_slim.read_field("slim_pll_cal_busy_status_trn_lsw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_cal_busy_status_trn_lsw: 0x{ts_reg:08X}")
        
        # SLIM PLL Calibration Busy Status (LSW): bits[31:0]
        # Status of the 8 SLIM PLL pll_cal_busysignals. 
        # Should normally be all False.
        ts_reg = self.ts_slim.read_field("slim_pll_cal_busy_status_lsw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_cal_busy_status_lsw: 0x{ts_reg:08X}")
        self.ts_reg = self.ts_reg + [ts_reg]

        # SLIM PLL Calibration Busy Transition (MSW): bits[23:0]
        # Indicates a transition of the 8 SLIM PLL pll_cal_busysignals.
        # Cleared by writing a '1' to this status bit.
        self.ts_slim.write_field("slim_pll_cal_busy_status_trn_msw", ts_slim_mask_msw)
        ts_reg = self.ts_slim.read_field("slim_pll_cal_busy_status_trn_msw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_cal_busy_status_trn_msw: 0x{ts_reg:06X}")
        
        # SLIM PLL Calibration Busy Status (MSW): bits[23:0]
        # Status of the 8 SLIM PLL pll_cal_busysignals. 
        # Should normally be all False.
        ts_reg = self.ts_slim.read_field("slim_pll_cal_busy_status_msw")
        self.checker.check(ts_reg == 0, f"{self.ts_name} slim_pll_cal_busy_status_msw: 0x{ts_reg:06X}")
        self.ts_reg = self.ts_reg + [ts_reg]

    def talon_slim_status_table(self):
        logging.info(f"Talon SLIM Status Summary")
        header_col = [ 
            "Present (LSW)",
            "Present (MSW)",
            "PLL Locked (LSW)",
            "PLL Locked (MSW)",
            "PLL Cal Busy (LSW)",
            "PLL Cal Busy (MSW)",
            ]
        table = BeautifulTable(maxwidth=200, precision=32)
        table.columns.header = header_col
        data_row = []
        for idx in range(0,len(self.ts_reg),1):
            data_row = data_row + [f"0x{self.ts_reg[idx]:08X}"]
        table.rows.append(data_row)
        logging.info(table)

def talon_slim_status(talon_status, checker):
    slim = TS_SLIM(talon_status, f"talon_slim_status", checker)
    slim.check_talon_slim_status()
    slim.talon_slim_status_table()

def main(talon_status):
    # bist_utils.Date().log_timestamp()
    checker = bist_utils.Checker()
    logging.info(f"#---------------------------------------------------------")
    logging.info(f"Talon-DX FPGA BIST testcase: Talon Status")
    talon_fault_status(talon_status, checker)
    talon_clock_status(talon_status, checker)
    talon_emif_status(talon_status, checker)
    talon_e100g_status(talon_status, checker)
    talon_slim_status(talon_status, checker)
    checker.report_log(f"Talon Status test results")
    return checker



if __name__ == "__main__":
    logging.info("tdc_base_bist_talon_status: __main__")
    import register_access as ra
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sys_json",                   help="The system map json file that details the register sets in the bitstream.")
    parser.add_argument("sys_ipmap",                  help="System map file that maps the VHDL hierarchy to a simpler name.")
    parser.add_argument("--mem",  metavar="DEV_FILE", help="The file to memory map to gain access to the registers. Defaults to /dev/mem", default="/dev/mem")

    args = parser.parse_args()
  
    # run register_access main():
    regsets = ra.main(args.mem, args.sys_json, args.sys_ipmap)
    talon_status = regsets.get("talon_status")
  
    #-------------------------------------------------------------------------
    # FPGA module BIST tests:
    #-------------------------------------------------------------------------
    # Talon Status: check the Talon Status 
    checker = main(talon_status)   