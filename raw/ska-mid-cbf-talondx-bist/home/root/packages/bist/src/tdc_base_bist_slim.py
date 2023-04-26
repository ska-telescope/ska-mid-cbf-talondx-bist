#!/usr/bin/python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1271 Add SLIM link self tests to the BIST script
#
# File Name: tdc_base_bist_slim.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script.
#
# BIST script for accessing FPGA registers. Note register_access.py is 
# imported to access the FPGA registers. The script is run directly on the 
# Talon board in Python stand-alone mode. 
# Test status is output to the Python logger utility.
#
# Date: 11 JAN 2023, developed during PI17
#
# args: <filename>.json and <filename>.ipmap files
#
# Run on talon board as follows:
# root@talon:~# 
#     python3 tdc_base_bist_slim.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#
# functions: 
# slim_config(slim_xcvr_phys, rx_loopback_mode) - acquires and initializes the 
#     defined SLIM Transceiver PHYs
#     inputs:
#     slim_xcvr_phys: 
#     rx_loopback_mode: 0 = external cable, 1 = interal XCVR PHY Rx serial 
#
# slim_bert(xcvr_phy, slim_xcvr_phys, runtime) - determines the SLIM XCVR PHY 
#     Rx Bit ERROR Rate (BER) in both internal and external loopback modes
# 
#-----------------------------------------------------------------------------
import sys
import time
import yaml
import tqdm
from beautifultable import BeautifulTable
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

import bist_utils


class SLIM_Transceiver_PHY:
    def __init__(self, regsets, tx_name, rx_name, mbo, chan) -> None:
        self.tx_slim = regsets.get(tx_name)
        self.rx_slim = regsets.get(rx_name)
        self.tx_name = tx_name
        self.rx_name = rx_name
        self.mbo = mbo
        self.chan = chan
        self.tx_word_count = 0
        self.tx_idle_word_count = 0
        self.rx_word_count = 0
        self.rx_idle_word_count = 0
        self.rx_idle_error_count = 0
        self.rx_ber = 0

    def tx_reset(self, reset_mode):
        """Reset the Stratix 10 H-tile Transceiver PHY IP Tx PCS and PMA blocks"""
        self.tx_slim.write_field("phy_reset", reset_mode & 0x1)
        reset_mode = self.tx_slim.read_field("phy_reset")
        logging.debug(f"{self.tx_name} PHY Reset state: {reset_mode}")

    def rx_reset(self, reset_mode):
        """Reset the Stratix 10 H-tile Transceiver PHY IP Rx PCS and PMA blocks"""
        self.rx_slim.write_field("phy_reset", reset_mode & 0x1)
        reset_mode = self.rx_slim.read_field("phy_reset")

    def read_xcvr_rate(self):
        """PHY data rate supported"""
        rx_rate = self.rx_slim.read_field("xcvr_rate")
        return rx_rate

    def read_counter_width(self):
        """counters that are read: word, packet, idle_word"""
        tx_cntr_width = self.tx_slim.read_field("counter_width")
        logging.debug(f"{self.tx_name} PHY Counter Width: {tx_cntr_width} bits")
        rx_cntr_width = self.rx_slim.read_field("counter_width")
        logging.debug(f"{self.rx_name} PHY Counter Width: {rx_cntr_width} bits")
        return rx_cntr_width

    def set_rx_loopback(self, lb_mode=False):
        """The assertion of the signal (rx_seriallpbk_en) enables the Tx to Rx
           serial loopback path within the transceiver.
           This is the 'serial loopback mode':
           Tx (PMA Serializer) -> Rx (Buffer -> PMA CDR -> Deserializer ...)"""
        self.rx_slim.write_field("serial_loopback_enable", lb_mode & 0x1)
        lb_mode = self.rx_slim.read_field("serial_loopback_enable")
        logging.debug(f"{self.rx_name} PHY Serial Loopback: {lb_mode}")

    def read_rx_loopback_reg(self):
        """serial loopback mode:
           # Tx (PMA Serializer) -> Rx (Buffer -> PMA CDR -> Deserializer ...)"""
        lb_mode = self.rx_slim.read_field("serial_loopback_enable")
        return lb_mode

    def clear_rx_cdr_lost_reg(self, clear_mode):
        rx_cdr_lost = self.rx_slim.read_field("cdr_lost")
        logging.debug(f"{self.rx_name} PHY CDR Lost: {rx_cdr_lost}")
        self.rx_slim.write_field("cdr_lost", clear_mode & 0x1)
        rx_cdr_lost = self.rx_slim.read_field("cdr_lost")
        logging.debug(f"{self.rx_name} PHY CDR Lost: {rx_cdr_lost}")

    def read_rx_cdr_lost_read_reg(self):
        rx_cdr_lost = self.rx_slim.read_field("cdr_lost")
        return rx_cdr_lost

    def read_rx_cdr_locked_reg(self):
        rx_cdr_locked = self.rx_slim.read_field("cdr_locked")
        return rx_cdr_locked

    def clear_rx_block_lost_reg(self, clear_mode):
        rx_block_lost = self.rx_slim.read_field("block_lost")
        logging.debug(f"{self.rx_name} PHY Block Lost: {rx_block_lost}")
        self.rx_slim.write_field("block_lost", clear_mode & 0x1)
        rx_block_lost = self.rx_slim.read_field("block_lost")
        logging.debug(f"{self.rx_name} PHY Block Lost: {rx_block_lost}")

    def read_rx_block_lost_reg(self):
        rx_block_lost = self.rx_slim.read_field("block_lost")
        return rx_block_lost

    def read_rx_block_aligned_reg(self):
        rx_block_aligned = self.rx_slim.read_field("block_aligned")
        return rx_block_aligned

    def read_support_user_idle_regs(self):
        tx_sup_user_idle = self.tx_slim.read_field("sup_user_idle")
        logging.debug(f"{self.tx_name} PHY Support User Idle: {tx_sup_user_idle}")
        rx_sup_user_idle = self.rx_slim.read_field("sup_user_idle")
        logging.debug(f"{self.rx_name} PHY Support User Idle: {rx_sup_user_idle}")

    def write_idle_ctrl_word_regs(self, tx_idle_ctrl_word, rx_idle_ctrl_word):
        self.tx_slim.write_field(
            "idle_ctrl_word", tx_idle_ctrl_word & 0x00FFFFFFFFFFFFFF
        )
        tx_idle_ctrl_word = self.tx_slim.read_field("idle_ctrl_word")
        logging.debug(
            f"{self.tx_name} PHY Idle Control Word: 0x{tx_idle_ctrl_word:016X}"
        )
        self.rx_slim.write_field(
            "idle_ctrl_word", rx_idle_ctrl_word & 0x00FFFFFFFFFFFFFF
        )
        rx_idle_ctrl_word = self.rx_slim.read_field("idle_ctrl_word")
        logging.debug(
            f"{self.rx_name} PHY Idle Control Word: 0x{rx_idle_ctrl_word:016X}"
        )

    def read_rx_idle_ctrl_word_reg(self, p_rx_idle_ctrl_word):
        rx_idle_ctrl_word = self.rx_slim.read_field("idle_ctrl_word")
        if rx_idle_ctrl_word == p_rx_idle_ctrl_word:
            logging.debug(
                f"{self.rx_name} PHY Idle Control Word: 0x{rx_idle_ctrl_word:016X}"
            )
        else:
            logging.debug(
                f"{self.rx_name} PHY Idle Control Word Error: 0x{rx_idle_ctrl_word:016X}"
            )
        return rx_idle_ctrl_word

    def clear_counters(self):
        self.tx_slim.write_field("clear_counters", 0x1)
        logging.debug(f"{self.tx_name} PHY Tx Counters Cleared")
        self.rx_slim.write_field("clear_counters", 0x1)
        logging.debug(f"{self.rx_name} PHY Rx Counters Cleared")

    def latch_counters(self):
        """shadow provides temporary write space so register bits can be appended to
           the same write transaction"""
        self.tx_slim.write_field("latch_counters", 0x1, shadow_only=True)
        self.tx_slim.write_field("clear_counters", 0x1)
        # clear residual bits set in the shadow register since they are currently maintained
        self.tx_slim.write_field("latch_counters", 0x0, shadow_only=True)
        self.tx_slim.write_field("clear_counters", 0x0)
        # logging.debug(f"{self.tx_name} PHY Tx Counters Latched-and-Cleared, Note: shadow register cleared")
        self.rx_slim.write_field("latch_counters", 0x1, shadow_only=True)
        self.rx_slim.write_field("clear_counters", 0x1)
        # clear residual bits set in the shadow register since they are currently maintained
        self.rx_slim.write_field("latch_counters", 0x0, shadow_only=True)
        self.rx_slim.write_field("clear_counters", 0x0)
        # logging.debug(f"{self.rx_name} PHY Rx Counters Latched-and-Cleared, Note: shadow register cleared")

    def read_packet_counters(self):
        tx_packet_cnt = self.tx_slim.read_field("packet_count")
        logging.debug(f"{self.tx_name} PHY Packet Counter: {tx_packet_cnt}")
        rx_packet_cnt = self.rx_slim.read_field("packet_count")
        logging.debug(f"{self.rx_name} PHY Packet Counter: {rx_packet_cnt}")
        return rx_packet_cnt

    def read_tx_word_count_reg(self):
        tx_word_cnt = self.tx_slim.read_field("word_count")
        return tx_word_cnt

    def read_rx_word_count_reg(self):
        rx_word_cnt = self.rx_slim.read_field("word_count")
        return rx_word_cnt

    def read_tx_idle_word_count_reg(self):
        tx_idle_word_cnt = self.tx_slim.read_field("idle_word_count")
        return tx_idle_word_cnt

    def read_rx_idle_word_count_reg(self):
        rx_idle_word_cnt = self.rx_slim.read_field("idle_count")
        return rx_idle_word_cnt

    def read_rx_idle_error_count_reg(self):
        rx_idle_error_cnt = self.rx_slim.read_field("idle_error_count")
        return rx_idle_error_cnt

    def read_rx_idle_error_counter(self):
        rx_idle_error_cnt = self.rx_slim.read_field("idle_error_count")
        return rx_idle_error_cnt

    def bit_error_rate_fcn(self):
        rx_idle_word_cnt = self.rx_slim.read_field("idle_count")
        rx_idle_error_cnt = self.rx_slim.read_field("idle_error_count")
        if rx_idle_word_cnt != 0:
            bit_error_rate = rx_idle_error_cnt / (
                rx_idle_word_cnt * 60.0
            )  # 60 bits/word
            logging.debug(
                f"{self.rx_name} PHY Bit Error Rate: {bit_error_rate} = {rx_idle_error_cnt}/{rx_idle_word_cnt*60.0}"
            )
            # bit_error_rate = rx_idle_error_cnt/(rx_idle_word_cnt)
            # logging.debug(f"{self.rx_name} PHY Word Error Rate: {bit_error_rate} = {rx_idle_error_cnt}/{rx_idle_word_cnt}")
            return bit_error_rate
        else:
            logging.debug(
                f"{self.rx_name} PHY Bit Error Rate: idle_word_count = 0, BER cannot be calculated"
            )
            logging.debug(
                f"{self.rx_name} PHY Bit Error Rate: ? = {rx_idle_error_cnt}/{rx_idle_word_cnt}"
            )

    def latch_rx_counters(self):
        """shadow_only provides temporary write space so register bits can be appended to
           the same write transaction"""
        self.rx_slim.write_field("latch_counters", 0x1, shadow_only=True)
        self.rx_slim.write_field("clear_counters", 0x1)
        # clear residual bits set in the shadow register since they are currently maintained
        self.rx_slim.write_field("latch_counters", 0x0, shadow_only=True)
        self.rx_slim.write_field("clear_counters", 0x0)
        # logging.debug(f"{self.rx_name} PHY Counters Latched-and-Cleared, Note: shadow register cleared")

    def xcvr_phy_init(self, rx_loopback_mode):
        # SLIM related definitons
        PHY_IDLE_CTRL_WORD = 0xE1856E442D4547  # 56 bits
        # PHY_IDLE_CTRL_WORD = 0x00000000000000  # 56 bits
        PHY_TX_IDLE_CTRL_WORD = PHY_IDLE_CTRL_WORD
        PHY_RX_IDLE_CTRL_WORD = PHY_IDLE_CTRL_WORD
        # Reset the PHY Tx Controller
        self.tx_reset(True)
        time.sleep(0.001)
        self.tx_reset(False)
        # Comfigure PHY for Serial Loopback Mode:
        # ---------------------------------------------------------------------
        # Set serial loopback before asserting PHY reset as the CDR PLL needs
        # to lock to the serial loopback Tx data stream
        # ---------------------------------------------------------------------
        self.set_rx_loopback(rx_loopback_mode)
        # ---------------------------------------------------------------------
        # Transceiver PHY Status Registers:
        # PHY Rx Clock Data Recovery (CDR) Lock Lost register
        self.clear_rx_cdr_lost_reg(True)
        # Transceiver PHY Rx CDR Lock Status register
        self.read_rx_cdr_locked_reg()
        # Transceiver PHY Rx 64b/66b Block Allignment Lost register
        self.clear_rx_block_lost_reg(True)
        # Transceiver PHY Rx 64b/66b Block Alignment Status register
        self.read_rx_block_aligned_reg()
        # Transceiver Tx/Rx Idle Control Word register
        self.write_idle_ctrl_word_regs(PHY_TX_IDLE_CTRL_WORD, PHY_RX_IDLE_CTRL_WORD)
        # Transceiver Rx Idle Control Word register
        self.read_rx_idle_ctrl_word_reg(PHY_RX_IDLE_CTRL_WORD)
        # ---------------------------------------------------------------------
        # Reset the PHY Rx Controller
        self.rx_reset(True)
        time.sleep(0.001)
        self.rx_reset(False)
        # Transceiver PHY CDR lock status register:
        self.read_rx_cdr_locked_reg()
        # Transceiver PHY Block lost status register:
        self.read_rx_block_aligned_reg()
        # Latch-and-Clear PHY Rx Counters  Note: shadow register cleared
        self.latch_rx_counters()


def slim_config(slim_xcvr_phys, rx_loopback_mode, regsets):
    """Acquire the Defined SLIM Transceiver PHYs and Initialize"""
    for idx in slim_xcvr_phys:
        mbo_list = idx.get("mbos")
        chan_list = idx.get("channels")

    xcvr_phy = dict()   # create an empty dictionary
    mbo_idx = 0
    for mbo in mbo_list:
        for chan in chan_list[mbo_idx]:
            tx_name = f"mbo{mbo}_chan{chan}_tx_slim"
            # logging.info(tx_name)
            rx_name = f"mbo{mbo}_chan{chan}_rx_slim"
            # logging.info(rx_name)
            if (tx_name in regsets) and (rx_name in regsets):
                xcvr_phy[f"mbo{mbo}_chan{chan}"] = SLIM_Transceiver_PHY(regsets, tx_name, rx_name, mbo, chan)
        mbo_idx += 1

    for chan_name, xcvr in xcvr_phy.items():
        logging.debug(f"SLIM PHY initialization: key = {chan_name}, value = {xcvr}")
        xcvr.xcvr_phy_init(rx_loopback_mode)

    return xcvr_phy

def slim_bert(xcvr_phy, slim_xcvr_phys, runtime, rx_loopback_mode, checker, current_time):
    """accumulate word and error counts for the BER caluculation
       where BER = rx_idle_error_count/(rx_idle_word_count x bits/word)"""

    if rx_loopback_mode:
        logging.info(f"SLIM BER test internal loopback mode [using XCVR PHY Rx serial loopback]")
    else:
        logging.info(f"SLIM BER test external loopback mode [using loopback cable]")

    for idx in slim_xcvr_phys:
        board = idx.get("board")
        mbo_list = idx.get("mbos")
        channel_list = idx.get("channels")
    
    BITS_PER_WORD = 60
    BIT_ERRORS_PER_WORD = 8  # assumes 1 bit error / byte
    BER_CHECK_THRESHOLD = 10**-10

    READ_TIME_SEC = 10.0  # 10.9 s before counters wrap
    bert_cntr = runtime
    
    if (runtime % READ_TIME_SEC) == 0:  
        additional_loops = 1
    else:
        additional_loops = 2
    LOOP_CNT = int(runtime / READ_TIME_SEC) + additional_loops
    # logging.info(f"(before loop) ----------------------------------- LOOP_CNT: {LOOP_CNT}")
    
    start = time.time()
    est_time = runtime
    logging.info(f"SLIM BER test will take approximately {est_time:1.1f} seconds ...")

    with tqdm.tqdm(total=est_time) as pbar:
        for lc in range(0, LOOP_CNT, 1):
            for xcvr_name, xcvr in xcvr_phy.items():
                xcvr.latch_counters()
                xcvr.tx_word_count = xcvr.tx_word_count + xcvr.read_tx_word_count_reg()
                xcvr.tx_idle_word_count = xcvr.tx_idle_word_count + xcvr.read_tx_idle_word_count_reg()
                xcvr.rx_word_count = xcvr.rx_word_count + xcvr.read_rx_word_count_reg()
                xcvr.rx_idle_word_count = xcvr.rx_idle_word_count + xcvr.read_rx_idle_word_count_reg()
                xcvr.rx_idle_error_count = xcvr.rx_idle_error_count + xcvr.read_rx_idle_error_count_reg()
                # Compute the Bit Error Rate (BER):
                # Note this is an estimate given we are using 60-bit words to calculate the BER
                if (not xcvr.rx_idle_word_count or (xcvr.rx_idle_error_count == xcvr.rx_idle_word_count)):
                    xcvr.rx_ber = 1.0
                elif not xcvr.rx_idle_error_count:
                    xcvr.rx_ber = 1/(xcvr.rx_idle_word_count*BITS_PER_WORD)
                else:
                    xcvr.rx_ber = xcvr.rx_idle_error_count/(xcvr.rx_idle_word_count*BIT_ERRORS_PER_WORD)
                # clear any residual bit errors before starting test
                if lc == 0:
                    xcvr.tx_word_count = 0
                    xcvr.tx_idle_word_count = 0
                    xcvr.rx_word_count = 0
                    xcvr.rx_idle_word_count = 0
                    xcvr.rx_idle_error_count = 0
                    xcvr.rx_ber = 0
                # check if channel BER is zero
                if lc == (LOOP_CNT - 1):
                    checker.check(xcvr.rx_ber <= BER_CHECK_THRESHOLD, f"{xcvr.rx_name} BER: {xcvr.rx_ber:.3e}")
                    # logging.info(f"{xcvr.rx_name} BER: {xcvr.rx_ber}")
            if lc == 0:
                if bert_cntr == 0:
                    break                            
                if bert_cntr <= READ_TIME_SEC:
                    # logging.info(f" ---- time.sleep({bert_cntr})")
                    time.sleep(bert_cntr)
                else:
                    bert_cntr = bert_cntr - READ_TIME_SEC
                    # logging.info(f" ---- time.sleep({READ_TIME_SEC})")
                    time.sleep(READ_TIME_SEC)
            else: 
                if lc < (LOOP_CNT - 1):
                    if bert_cntr <= READ_TIME_SEC:
                        # logging.info(f" ---- time.sleep({bert_cntr})")
                        time.sleep(bert_cntr)
                    else:
                        bert_cntr = bert_cntr - READ_TIME_SEC
                        # logging.info(f" ---- time.sleep({READ_TIME_SEC})")
                        time.sleep(READ_TIME_SEC)
            pbar.update(READ_TIME_SEC)

    end = time.time()
    logging.info(f"SLIM BER test finished in {end-start:1.1f} seconds.")

    # Display the Transceiver PHY Rx Status and Bit Error Rate (BER)
    # Mid-Board Optical (MBO)
    # Loopback: 0 = external, 1 = Rx serial (internal)
    # Clock Data Recovery (CDR): 0 = False, 1 = True
    # Block Aligned (BA): 0 = False, 1 = True
    # Bit Error Rate (BER)
    logging.info(f"SLIM Loopback Test Summary")
    leap_obt = [1, 2, 3, 4, 5,]  # PCB LEAP On-Board Transcievers (OBTs) mapping

    influx_csv_writer = bist_utils.influx_csv('tdc_base_bist_logfile.csv')
    data_type = ['measurement','tag','tag','long','long','string','string','string','string','string','long','long','long','long','long','string','datetime:RFC3339']
    influx_csv_writer.write_datatype(data_type)

    header_col = [
        "Register",
        "LEAP",
        "MBO",
        "Chan",
        "Rate (Gbps)",
        "Loopback",
        "CDR Lost",
        "CDR",
        "BA Lost",
        "BA",
        "Tx Data Words",
        "Tx Idle Words",
        "Rx Data Words",
        "Rx Idle Words",
        "Rx Idle Errors",
        "Estimated BER",
    ]

    table = BeautifulTable(maxwidth=200, precision=32)
    table.columns.header = header_col
    influx_csv_writer.write_header(header_col)
    for xcvr_name, xcvr in xcvr_phy.items():
        data_row = ['talon_ber_status']
        data_row = (
            data_row
            + [leap_obt[xcvr.mbo - 1]]
            + [xcvr.mbo]
            + [xcvr.chan]
            + [xcvr.read_xcvr_rate()]
            + [xcvr.read_rx_loopback_reg()]
            + [xcvr.read_rx_cdr_lost_read_reg()]
            + [xcvr.read_rx_cdr_locked_reg()]
            + [xcvr.read_rx_block_lost_reg()]
            + [xcvr.read_rx_block_aligned_reg()]
            + [xcvr.tx_word_count]
            + [xcvr.tx_idle_word_count]
            + [xcvr.rx_word_count]
            + [xcvr.rx_idle_word_count]
            + [xcvr.rx_idle_error_count]
            + [f"{xcvr.rx_ber:.3e}"]
        )
        table.rows.append(data_row)
        influx_csv_writer.write_csv(data_row, current_time)
    logging.info(table)

def main(slim_xcvr_phys, slim_xcvr_phy_loopback_mode, runtime, regsets, current_time):
    # bist_utils.Date().log_timestamp()
    checker = bist_utils.Checker()
    logging.info(f"#---------------------------------------------------------")
    logging.info(f"Talon-DX FPGA BIST testcase: SLIM")
    # configure the SLIM XCVR PHYs
    xcvr_phy = slim_config(slim_xcvr_phys, slim_xcvr_phy_loopback_mode, regsets)
    # run the transceiver PHY Rx cummulative bit error rate test (BER)
    slim_bert(xcvr_phy, slim_xcvr_phys, runtime, slim_xcvr_phy_loopback_mode, checker, current_time)
    checker.report_log(f"SLIM loopback test results")
    # clear the serial loopback 
    for xcvr_name, xcvr in xcvr_phy.items():
        xcvr.set_rx_loopback(False)
    return checker
 



if __name__ == "__main__":
    logging.info("tdc_base_bist_slim: __main__")
    import register_access as ra
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sys_json",                   help="The system map json file that details the register sets in the bitstream.")
    parser.add_argument("sys_ipmap",                  help="System map file that maps the VHDL hierarchy to a simpler name.")
    parser.add_argument("--mem",  metavar="DEV_FILE", help="The file to memory map to gain access to the registers. Defaults to /dev/mem", default="/dev/mem")

    args = parser.parse_args()
    # run register_access main() to acquire regsets:
    regsets = ra.main(args.mem, args.sys_json, args.sys_ipmap)
    
    # BIST arguments (hardcoded)
    args = dict(
        testcase = "SLIM XCVR Int_LB",
        slim_runtime = 1.0,      # test time in seconds
        # SLIM Transceiver PHYS:
        slim_xcvr_phys = [
        {
            'board': "talon", 
            "mbos": [1, ],  
            "channels": [ [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,], ],
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
    assert ((testcase == "SLIM XCVR Int_LB") or (testcase == "SLIM XCVR Ext_LB")), \
            f"SLIM Transceiver BIST: {testcase} testcase not found"        
    runtime = args.get('slim_runtime')
    slim_xcvr_phys = args.get('slim_xcvr_phys') 

    #-------------------------------------------------------------------------
    # FPGA module SLIM Transceiver PHY BIST test:
    #-------------------------------------------------------------------------
    # SLIM XCVR PHY loopback mode: 0 = external, 1 = Rx serial
    if testcase == "SLIM XCVR Int_LB":
        slim_xcvr_phy_loopback_mode = 1
    elif testcase == "SLIM XCVR Ext_LB":
            slim_xcvr_phy_loopback_mode = 0
    else:
        logging.error(f"Invalid testcase {testcase}!")
    
    checker = main(slim_xcvr_phys, slim_xcvr_phy_loopback_mode, runtime, regsets)    