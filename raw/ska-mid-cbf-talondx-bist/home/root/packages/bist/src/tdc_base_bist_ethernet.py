#!/usr/bin/python3
#
#-----------------------------------------------------------------------------
# JIRA CIP-1282 Add 100G Ethernet self-tests to the BIST script
#
# File Name: tdc_base_bist_ethernet.py
# 
# Description: Python Built-In Self Test (BIST) talon board verification 
# script - 100GbE.
#
# BIST script for accessing FPGA registers. Note register_access.py is 
# imported to access the FPGA registers. The script is run directly on the 
# Talon board in Python stand-alone mode. 
# Test status is output to the Python logger utility.
#
# Date: 18 JAN 2023, developed during PI17
#
# args: <filename>.json and <filename>.ipmap files
#
# Run on talon board as follows:
# root@talon:~# 
#     python3 tdc_base_bist_ethernet.py ./talon_dx-tdc_base.json ./tdc.ipmap 
#
# functions: 
# [phy, stats, fec] = eth_100G_config(Eth_100G_IP_cores, eth_phy_loopback_mode)
# eth_100G_error_test(phy, stats, fec, Eth_100G_IP_cores, runtime, eth_phy_loopback_mode)
# 
# References:
# 1. UG-20085, Low Latency 100G Ethernet Intel FPGA IP Core User Guide
#    For Intel Stratix 10 Devices., Intel, February 2022, Sec. 8.
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

class ETH_PHY:
    def __init__(self, regsets, eth_phy_name, checker) -> None:
        self.eth_phy = regsets.get(eth_phy_name) 
        self.eth_phy_name = eth_phy_name
        self.checker = checker

    def check_phy_revid_reg(self):
        # REVID: bits[31:0]
        # IP core PHY module revision ID
        id_reg = self.eth_phy.read_field("REVID")
        self.checker.check(id_reg == 0x08092017, f"{self.eth_phy_name} REVID: 0x{id_reg:08X}")

    def check_phy_scratch_reg(self):
        # SCRATCH: bits[31:0]
        # Scratch register available for testing
        self.eth_phy.write_field("scratch", 0x00000000)
        scratch_reg = self.eth_phy.read_field("scratch")
        self.checker.check(scratch_reg == 0x00000000, f"{self.eth_phy_name} scratch: 0x{scratch_reg:08X}")
        self.eth_phy.write_field("scratch", 0xE1E1E1E1)
        scratch_reg = self.eth_phy.read_field("scratch")
        self.checker.check(scratch_reg == 0xE1E1E1E1, f"{self.eth_phy_name} scratch: 0x{scratch_reg:08X}")
        self.eth_phy.write_field("scratch", 0x1E1E1E1E)
        scratch_reg = self.eth_phy.read_field("scratch")
        self.checker.check(scratch_reg == 0x1E1E1E1E, f"{self.eth_phy_name} scratch: 0x{scratch_reg:08X}")

    def check_phy_name_regs(self):   
        # PHY_NAME_0: bits[31:0]
        # First characters of IP core variation identifier string, "100". 
        id_reg = self.eth_phy.read_field("phy_name_0") 
        self.checker.check(id_reg == 0x00313030, f"{self.eth_phy_name} phy_name_0: 0x{id_reg:08X}")
        # PHY_NAME_1: bits[31:0]
        # Next characters of IP core variation identifier string, "GE".
        id_reg = self.eth_phy.read_field("phy_name_1") 
        self.checker.check(id_reg == 0x00004745, f"{self.eth_phy_name} phy_name_1: 0x{id_reg:08X}")
        # PHY_NAME_2: bits[31:0]
        # Final characters of IP core variation identifier string, "pcs".
        id_reg = self.eth_phy.read_field("phy_name_2") 
        self.checker.check(id_reg == 0x00706373, f"{self.eth_phy_name} phy_name_2: 0x{id_reg:08X}")

        # PHY_CONFIG
        # PHY configuration registers. The following bit fields are defined:
    def reset_phy(self, val=False):
        # Bit[0]: eio_sys_rst. Full system reset (except registers). 
        # Set this bit to initiate the internal reset sequence.
        self.eth_phy.write_field("eio_sys_rst", val) 
        phy_config_reg = self.eth_phy.read_field("eio_sys_rst") 
        logging.debug(f"{self.eth_phy_name} eio_sys_rst: {phy_config_reg}")
    def reset_phy_soft_txp(self, val=False):
        # Bit[1]: soft_txp_rst. TX soft reset.
        self.eth_phy.write_field("soft_txp_rst", val) 
        phy_config_reg = self.eth_phy.read_field("soft_txp_rst") 
        logging.info(f"{self.eth_phy_name} soft_txp_rst: {phy_config_reg}")
    def reset_phy_soft_rxp(self, val=False):
        # Bit[2]: soft_rxp_rst. RX soft reset.
        self.eth_phy.write_field("soft_rxp_rst", val) 
        phy_config_reg = self.eth_phy.read_field("soft_rxp_rst") 
        logging.info(f"{self.eth_phy_name} soft_rxp_rst: {phy_config_reg}")
        # Bit[3]: Reserved.
    def set_phy_lock_to_ref_clock(self, val=False):
        # Bit[4]: set_ref_lock. Directs the RX CDR PLL to lock to the 
        # reference clock.
        self.eth_phy.write_field("set_ref_lock", val) 
        phy_config_reg = self.eth_phy.read_field("set_ref_lock") 
        logging.info(f"{self.eth_phy_name} set_ref_lock: {phy_config_reg}")
    def set_phy_lock_to_data(self, val=False):
        # Bit[5]: set_data_lock. Directs the RX CDR PLL to lock to data.
        self.eth_phy.write_field("set_data_lock", val) 
        phy_config_reg = self.eth_phy.read_field("set_data_lock") 
        logging.info(f"{self.eth_phy_name} set_data_lock: {phy_config_reg}")
        # Bits[31:6]: Reserved.
        # The reset bits are not self-clearing. To force a reset, you can set 
        # and reset a reset bit in back-to-back register write operations.

    def read_phy_word_lock_reg(self):
        # WORD_LOCK: bits[19:0]
        # Each of the 20 lower order bits, when asserted, indicates that the
        # corresponding virtual channel has identified 66 bit block boundaries
        # in the serial data stream.
        word_lock_reg = self.eth_phy.read_field("word_lock")
        logging.debug(f"{self.eth_phy_name} word_lock: 0x{word_lock_reg:05X}")
        return word_lock_reg

    def set_phy_loopback(self, lb_mode=False):
        # EIO_SLOOP: bits[3:0]
        # Serial PMA loopback. Setting a bit [4'b1] puts the 
        # corresponding transceiver [100Gb = 4x25Gb] in serial loopback mode. 
        # In serial loopback mode, the TX lane loops back to the RX lane on 
        # an internal loopback path.
        # Tx (PMA Serializer) -> Rx (Buffer -> PMA CDR -> Deserializer ...)
        if lb_mode == True:
            lb_val = 0xF 
        else:
            lb_val = 0x0
        self.eth_phy.write_field("eio_sloop", lb_val & 0xF)
        lb_val_reg = self.eth_phy.read_field("eio_sloop")
        logging.debug(f"{self.eth_phy_name} PHY Serial Loopback: 0x{lb_val_reg:01X}")

    def read_phy_loopback_reg(self):
        # EIO_SLOOP: bits[3:0]
        # Tx (PMA Serializer) -> Rx (Buffer -> PMA CDR -> Deserializer ...)
        # Tx lane[1..4] loops back to the Rx lane[1..4] on an internal loopback path.
        lb_val_reg = self.eth_phy.read_field("eio_sloop")
        logging.debug(f"{self.eth_phy_name} PHY Serial Loopback: 0x{lb_val_reg:01X}")
        return lb_val_reg

    def read_phy_freq_lock_reg(self):
        # EIO_FREQ_LOCK: bits[3:0]
        # Each of the lower order four bits, when asserted, indicates that 
        # the corresponding lane RX clock data recovery (CDR) phaselocked 
        # loop (PLL) is locked.
        freq_lock_reg = self.eth_phy.read_field("eio_freq_lock")
        logging.debug(f"{self.eth_phy_name} eio_freq_lock: 0x{freq_lock_reg:01X}")
        return freq_lock_reg

    def check_phy_clk(self):
        phy_clk_passed = 0
        phy_clk_failed = 0
        # PHY_CLK 
        # The following encodings are defined:
        # Bit[0]: If set to 1, indicates the TX transceivers have completed
        # reset.
        phy_clk_reg = self.eth_phy.read_field("tx_reset_done")
        logging.info(f"{self.eth_phy_name} tx_reset_done {phy_clk_reg}")
        if phy_clk_reg == True:
            phy_clk_passed += 1
        else:
            phy_clk_failed += 1
        # Bit[1]: If set to 1, indicates the TX core clock is stable. And if
        # the Enable RS-FEC is turned on, the FEC TX PLL has acquired frequency
        # lock.
        phy_clk_reg = self.eth_phy.read_field("tx_core_clock_stable")
        logging.info(f"{self.eth_phy_name} tx_core_clock_stable {phy_clk_reg}")
        if phy_clk_reg == True:
            phy_clk_passed += 1
        else:
            phy_clk_failed += 1
        # Bit[2]: If set to 1, indicates the RX core clock is stable. And if 
        # the Enable RS-FEC is turned on, the FEC RX PLL has acquired frequency
        # lock.
        phy_clk_reg = self.eth_phy.read_field("rx_core_clock_stable")
        logging.info(f"{self.eth_phy_name} rx_core_clock_stable {phy_clk_reg}")
        if phy_clk_reg == True:
            phy_clk_passed += 1
        else:
            phy_clk_failed += 1
        self.checker.check(
            (phy_clk_passed > 0 and phy_clk_failed == 0),
            f"PHY_CLK status: checks passed: {phy_clk_passed}, checks failed: {phy_clk_failed}",
            True,
            )

    def read_phy_frame_error_reg(self):
        # FRM_ERR: bits[19:0] 
        # Each of the 20 lower order bits, when asserted, indicates that the 
        # corresponding virtual lane has a frame error. You can read this 
        # register to determine if the IP core sustains a low number of frame
        # errors, below the threshold to lose word lock. These bits are sticky,
        # unless the virtual lane loses word lock. Write 1'b1 to the
        # SCLR_FRM_ERR register to clear.
        # If a virtual lane loses word lock, it clears the corresponding 
        # register bit. Each bit in this register has a valid value only if the
        # corresponding bit in the WORD_LOCK register at offset 0x312 has the
        # value of 1.
        frm_err_reg = self.eth_phy.read_field("frm_err")
        logging.debug(f"{self.eth_phy_name} frm_err: 0x{frm_err_reg:05X}")
        return frm_err_reg

    def clear_phy_frame_errors(self):
        # SCLR_FRM_ERR: bits[31:0]
        # Synchronous clear for FRM_ERR register. Write 1'b1 to this register 
        # to clear the FRM_ERR register and bit [1] of the LANE_DESKEWED
        # register. A single bit clears all sticky framing errors. This bit
        # does not auto clear. Write a 1'b0 to continue logging frame errors.
        self.eth_phy.write_field("sclr_frm_err", 0x00000001)
        # link_db_reg = self.eth_phy.read_field("sclr_frm_err")
        # logging.debug(f"{self.eth_phy_name} sclr_frm_err: 0x{link_db_reg:08X}")

    def log_phy_frame_errors(self):
        # SCLR_FRM_ERR: bits[31:0]
        # Synchronous clear for FRM_ERR register. Write 1'b1 to this register 
        # to clear the FRM_ERR register and bit [1] of the LANE_DESKEWED
        # register. A single bit clears all sticky framing errors. This bit
        # does not auto clear. Write a 1'b0 to continue logging frame errors.
        self.eth_phy.write_field("sclr_frm_err", 0x00000000)
        link_db_reg = self.eth_phy.read_field("sclr_frm_err")
        logging.debug(f"{self.eth_phy_name} sclr_frm_err: 0x{link_db_reg:08X}")

    def read_phy_khz_rx_reg(self):
        # KHZ_RX: bits[31:0]
        # RX clock (clk_rxmac) frequency in kHz, assuming the clk_status clock 
        # has the frequency of 100 MHz. The RX clock frequency is the value in
        # this register times the frequency of the clk_status clock, divided by
        # 100.
        khz_rx_reg = self.eth_phy.read_field("khz_rx")
        logging.debug(f"{self.eth_phy_name} khz_rx: {khz_rx_reg} kHz")

    def read_phy_khz_tx_reg(self):
        # KHZ_TX: bits[31:0]
        # RX clock (clk_txmac) frequency in kHz, assuming the clk_status clock 
        # has the frequency of 100 MHz. The TX clock frequency is the value in
        # this register times the frequency of the clk_status clock, divided by
        # 100.
        khz_tx_reg = self.eth_phy.read_field("khz_tx")
        logging.debug(f"{self.eth_phy_name} khz_tx: {khz_tx_reg} kHz")

    def read_phy_enable_rsfec_reg(self):
        # ENABLE_RSFEC: bits[31:0] (1'b1 is the enable bit)
        # Reed-Solomon Foward Error Correction (RS-FEC) enable register
        # When the RS-FEC block is enabled, writing 1 enables the RS-FEC 
        # data path and writing 0 disables the RS-FEC data path.
        # Note FEC is always enabled for QSFP28 connections
        rs_fec_reg = self.eth_phy.read_field("enable_rsfec")
        logging.debug(f"{self.eth_phy_name} enable_rsfec: 0x{rs_fec_reg:08X}")

    def check_phy_regs(self):
        self.check_phy_revid_reg()
        self.check_phy_name_regs()
        self.check_phy_scratch_reg()

    def config_phy_link_regs(self, loopback_mode):
        self.reset_phy(True)
        time.sleep(0.001)
        self.reset_phy(False)
        time.sleep(0.010)   # short delay before checking PHY 'tx_reset_done'
        self.check_phy_clk()
        self.read_phy_khz_rx_reg()
        self.read_phy_khz_tx_reg()
        self.set_phy_loopback(loopback_mode)
        self.read_phy_enable_rsfec_reg()
        self.read_phy_frame_error_reg()
        self.clear_phy_frame_errors()
        self.log_phy_frame_errors()
        self.read_phy_frame_error_reg()


class ETH_Statistics:
    def __init__(self, regsets, tx_name, rx_name) -> None:
        self.eth_tx_stats = regsets.get(tx_name)  
        self.eth_rx_stats = regsets.get(rx_name)  
        self.tx_stats_name = tx_name
        self.rx_stats_name = rx_name

    def read_stats_cntr_fcs_regs(self):
        # CNTR_TX_FCS, CNTR_RX_FCS: bits [63:0]
        # Num transmitted packets with Frame Check Sequence (FCS) (CRC-32) errors 
        tx_cntr_fcs_reg = self.eth_tx_stats.read_field("cntr_tx_fcs") # 64 bits
        logging.debug(f"{self.tx_stats_name} cntr_tx_fcs: {tx_cntr_fcs_reg}")
        # Num received packets with Frame Check Sequence (FCS) (CRC-32) errors 
        rx_cntr_fcs_reg = self.eth_rx_stats.read_field("cntr_rx_fcs") # 64 bits
        logging.debug(f"{self.rx_stats_name} cntr_rx_fcs: {rx_cntr_fcs_reg}")
        return [tx_cntr_fcs_reg, rx_cntr_fcs_reg]

    def eth_stats_cntr_tx_fcs(self):
        # CNTR_TX_FCS: bits [63:0]
        # Num transmitted packets with Frame Check Sequence (FCS) (CRC-32) errors 
        tx_cntr_fcs_reg = self.eth_tx_stats.read_field("cntr_tx_fcs") # 64 bits
        logging.debug(f"{self.tx_stats_name} cntr_tx_fcs: {tx_cntr_fcs_reg}")
        return tx_cntr_fcs_reg

    def read_stats_rx_fcs_cntr_reg(self):
        # CNTR_RX_FCS: bits [63:0]
        # Num received packets with Frame Check Sequence (FCS) (CRC-32) errors 
        rx_cntr_fcs_reg = self.eth_rx_stats.read_field("cntr_rx_fcs") # 64 bits
        return rx_cntr_fcs_reg

    # CNTR_TX/RX_CONFIG: bits[2:0]
    # Configuration of TX/RX statistics counters:
    # Bits[31:3] are Reserved.
    # Bit[2]: Shadow request (active high): When set to the value of
    # 1, TX/RX statistics collection is paused. The underlying counters
    # continue to operate, but the readable values reflect a snapshot
    # at the time the pause flag was activated. Write a 0 to release.
    def write_stats_shadow_req_reg(self, val=False):
        # 0: latest counter values, 1: snapshot of counter values
        self.eth_tx_stats.write_field("tx_shadow_req", val)        
        self.eth_rx_stats.write_field("rx_shadow_req", val)        
    # Bit[1]: Parity-error clear. When software sets this bit, the IP
    # core clears the parity bit CNTR_TX/RX_STATUS[0]. This bit
    # (CNTR_TX/RX_CONFIG[1]) is self-clearing.
    def clear_stats_parity_errors(self, val=False):
        self.eth_tx_stats.write_field("tx_parity_err_clr", val)        
        self.eth_rx_stats.write_field("rx_parity_err_clr", val)        
    # Bit[0]: Software can set this bit to the value of 1 to reset all of
    # the TX/RX statistics registers at the same time. This bit is selfclearing.
    def clear_stats_counters(self, val=False):
        self.eth_tx_stats.write_field("tx_cnt_clr", val)        
        self.eth_rx_stats.write_field("rx_cnt_clr", val)        

    # CNTR_TX/RX_STATUS: bits[1:0]
    # Bits[31:2] are Reserved.
    # Bit[1]: Indicates that the TX/RX statistics registers are paused (while
    # CNTR_TX/RX_CONFIG[2] is asserted).
    def read_stats_cnt_pause_regs(self):
        tx_cnt_pause_reg = self.eth_tx_stats.read_field("tx_cnt_pause")        
        rx_cnt_pause_reg = self.eth_rx_stats.read_field("rx_cnt_pause")        
    # Bit[0]: Indicates the presence of at least one parity error in the
    # TX/RX statistics counters.
    def read_stats_parity_err_regs(self):
        tx_parity_err_reg = self.eth_tx_stats.read_field("tx_parity_err")        
        logging.debug(f"{self.tx_stats_name} tx_parity_error: {tx_parity_err_reg}")
        rx_parity_err_reg = self.eth_rx_stats.read_field("rx_parity_err")        
        logging.debug(f"{self.rx_stats_name} rx_parity_error: {rx_parity_err_reg}")

    def read_stats_tx_parity_err_reg(self):
        tx_parity_err_reg = self.eth_tx_stats.read_field("tx_parity_err")        
        logging.debug(f"{self.tx_stats_name} tx_parity_error: {tx_parity_err_reg}")
        return tx_parity_err_reg

    def read_stats_rx_parity_err_reg(self):
        rx_parity_err_reg = self.eth_rx_stats.read_field("rx_parity_err")        
        logging.debug(f"{self.rx_stats_name} rx_parity_error: {rx_parity_err_reg}")
        return rx_parity_err_reg

    def read_stats_rx_counters(self):
        logging.info(f"100G Ethernet {self.rx_stats_name} Counter Registers:")
        self.eth_rx_stats.write_field("rx_shadow_req", 1)
        logging.info(f"\t\tcntr_rx_64b:         {self.eth_rx_stats.read_field('cntr_rx_64b')}")
        logging.info(f"\t\tcntr_rx_65to127b:    {self.eth_rx_stats.read_field('cntr_rx_65to127b')}")
        logging.info(f"\t\tcntr_rx_128to255b:   {self.eth_rx_stats.read_field('cntr_rx_128to255b')}")
        logging.info(f"\t\tcntr_rx_256to511b:   {self.eth_rx_stats.read_field('cntr_rx_256to511b')}")
        logging.info(f"\t\tcntr_rx_512to1023b:  {self.eth_rx_stats.read_field('cntr_rx_512to1023b')}")
        logging.info(f"\t\tcntr_rx_1024to1518b: {self.eth_rx_stats.read_field('cntr_rx_1024to1518b')}")
        logging.info(f"\t\tcntr_rx_1519tomaxb:  {self.eth_rx_stats.read_field('cntr_rx_1519tomaxb')}")
        logging.info(f"\t\tcntr_rx_oversize:    {self.eth_rx_stats.read_field('cntr_rx_oversize')}")
        logging.info(f"\t\trxFrameOctetsOK:     {self.eth_rx_stats.read_field('rxframeoctetsok')}")
        self.eth_rx_stats.write_field("rx_shadow_req", 0)

    def read_stats_tx_counters(self):
        logging.info(f"100G Ethernet {self.tx_stats_name} Counter Registers:")
        self.eth_tx_stats.write_field("tx_shadow_req", 1)
        logging.info(f"\t\tcntr_tx_64b:         {self.eth_tx_stats.read_field('cntr_tx_64b')}")
        logging.info(f"\t\tcntr_tx_65to127b:    {self.eth_tx_stats.read_field('cntr_tx_65to127b')}")
        logging.info(f"\t\tcntr_tx_128to255b:   {self.eth_tx_stats.read_field('cntr_tx_128to255b')}")
        logging.info(f"\t\tcntr_tx_256to511b:   {self.eth_tx_stats.read_field('cntr_tx_256to511b')}")
        logging.info(f"\t\tcntr_tx_512to1023b:  {self.eth_tx_stats.read_field('cntr_tx_512to1023b')}")
        logging.info(f"\t\tcntr_tx_1024to1518b: {self.eth_tx_stats.read_field('cntr_tx_1024to1518b')}")
        logging.info(f"\t\tcntr_tx_1519tomaxb:  {self.eth_tx_stats.read_field('cntr_tx_1519tomaxb')}")
        logging.info(f"\t\tcntr_tx_oversize:    {self.eth_tx_stats.read_field('cntr_tx_oversize')}")
        logging.info(f"\t\ttxFrameOctetsOK:     {self.eth_tx_stats.read_field('txframeoctetsok')}")
        self.eth_tx_stats.write_field("tx_shadow_req", 0)

    def read_stats_counters(self):
        self.read_stats_tx_counters()
        self.read_stats_rx_counters()

    def config_stats_regs(self):
        self.clear_stats_counters(True)
        self.clear_stats_parity_errors(True)
        self.read_stats_parity_err_regs()
    
    def read_stats_errors(self):
        self.read_stats_parity_err_regs()
        self.read_stats_cntr_fcs_regs()


class ETH_RSFEC:
    def __init__(self, regsets, tx_name, rx_name) -> None:
        self.eth_tx_fec = regsets.get(tx_name)
        self.eth_rx_fec = regsets.get(rx_name)
        self.tx_fec_name = tx_name
        self.rx_fec_name = rx_name
        self.rx_fec_corr_cw_cntr = 0
        self.rx_fec_uncorr_cw_cntr = 0

    def enable_fec_tx_error_insertion_single(self, val=False):
        # ERR_INS_EN: bit[4]
        # Enable error insertion for single FEC codeword. This bit selfclears
        # after the Reed-Solomon FEC transmitter inserts the error.
        self.eth_tx_fec.write_field("err_ins_single", val)
        logging.debug(f"{self.tx_fec_name} Tx FEC codeword error insertion single: {val}")

    def enable_fec_tx_error_insertion_all(self, val=False):
        # ERR_INS_EN: bit[0]
        # Enable error insertion for every FEC codeword. 
        # Specifies that the Reed-Solomon FEC transmitter should insert the 
        # error in every FEC codeword.
        self.eth_tx_fec.write_field("err_ins_all", val)
        logging.debug(f"{self.tx_fec_name} Tx FEC codeword error insertion all: {val}")

    def read_fec_tx_error_insertion_all_reg(self):
        # ERR_INS_EN: bit[0]
        # Enable error insertion for every FEC codeword. 
        # Specifies that the Reed-Solomon FEC transmitter should insert the 
        # error in every FEC codeword.
        err_ins_all_reg = self.eth_tx_fec.read_field("err_ins_all")
        return err_ins_all_reg

    def config_fec_tx_error_mask(self):
        # SYM_32: bit[24]
        # Each FEC codeword consists of 16 groups of 33 symbols. This
        # register field specifies whether the RSFEC transmitter corrupts 
        # symbol 32 (of symbols 0-32) in each corrupted group. Specifically, 
        # the value of 1 directs the IP core to corrupt symbol 32 according to
        # BIT_MASK.
        self.eth_tx_fec.write_field("sym_32", True)
        # BIT_MASK: bits[17:8]
        # Specifies which of the ten bits the RS-FEC transmitter 
        # corrupts in each corrupted symbol. Specifically, the value of 1 in 
        # bit [n+8] directs the IP core to corrupt bit [n] in each corrupted 
        # symbol.
        self.eth_tx_fec.write_field("bit_mask", 0x001) 
        # GROUP_NUM: bits[3:0]
        # Each FEC codeword consists of 16 groups of 33 symbols. This register
        # field specifies the single group of 33 symbols that the RS-FEC 
        # transmitter corrupts in the current FEC codeword.
        self.eth_tx_fec.write_field("group_num", 0x0)

    def config_fec_tx_symbol_error_mask(self):
        # SYMBOL_ERR_MASK: bits[31:0]
        # Each FEC codeword consists of 16 groups of 33 symbols. This register
        # specifies which of the lower order 32 symbols in a group the RS-FEC
        # transmitter corrupts. Specifically the value of 1 in bit [n] directs
        # the IP core to corrupt symbol n.    
        self.eth_tx_fec.write_field("symbol_err_mask", 0x00000001)

    def read_fec_rx_corr_cw_cntr_reg(self):
        # CORRECTED_CW: bits[31:0]
        # 32-bit counter that contains the number of corrected FEC codewords
        # processed. The value resets to zero upon read and holds at max count.
        rx_corr_cw_reg = self.eth_rx_fec.read_field("corrected_cw")
        # logging.info(f"{self.rx_fec_name} FEC Rx corrected codewords: {rx_corr_cw_reg}")
        return rx_corr_cw_reg

    def read_fec_rx_uncorr_cw_cntr_reg(self):
        # UNCORRECTED_CW: bits:[31:0]
        # 32-bit counter that contains the number of uncorrected FEC codewords
        # processed. The value resets to zero upon read and holds at max count.
        rx_uncorr_cw_reg = self.eth_rx_fec.read_field("uncorrected_cw") 
        # logging.info(f"{self.rx_fec_name} FEC Rx uncorrected codewords: {rx_uncorr_cw_reg}")
        return rx_uncorr_cw_reg
    
    def config_fec_regs(self):
        # disable FEC TX error insertion 
        self.enable_fec_tx_error_insertion_single(False)
        self.enable_fec_tx_error_insertion_all(False)
        # clear any residual codewords
        self.read_fec_rx_corr_cw_cntr_reg()
        self.read_fec_rx_uncorr_cw_cntr_reg()

    def insert_fec_errors(self):
        # enable FEC TX error insertion 
        self.config_fec_tx_error_mask()
        self.config_fec_tx_symbol_error_mask()
        self.enable_fec_tx_error_insertion_single(False)
        self.enable_fec_tx_error_insertion_all(True)


class ETH_QSFP:
    def __init__(self, regsets, qsfp_name) -> None:
        self.qsfp = regsets.get(qsfp_name)
        self.qsfp_name = qsfp_name
        self.qsfp_config_valid = False

    def enable_n_qsfp_module(self, val=False):
        # When set to '0', the QSFP module responds to 2-wire serial 
        # communication commands. When set to '1' the module does not respond
        # to or acknowledge any 2-wire interface communication from the host. 
        # This allows the use of multiple QSFP module on a single 2-wire bus.
        self.qsfp.write_field("mod_sel_n", val)
        qsfp_reg = self.qsfp.read_field("mod_sel_n")
        logging.debug(f"{self.qsfp_name} mod_sel_n: {qsfp_reg}")

    def reset_n_qsfp(self, val=True):
        # Toggling this field to '0' then back to '1' initiates a complete QSFP
        # module reset, returning all user module settings to their default
        # state. The module indicates completion of reset by posting an 
        # interrupt signal.
        self.qsfp.write_field("reset_n", val)
        qsfp_reg = self.qsfp.read_field("reset_n")
        logging.debug(f"{self.qsfp_name} reset_n: {qsfp_reg}")

    def set_qsfp_low_power_mode(self, val=False):
        # Setting this field to '1' sets the module in low-power mode. 
        # This disables the laser and receiver but keeps the I2C accessable.
        self.qsfp.write_field("lowpwr", val)
        qsfp_reg = self.qsfp.read_field("lowpwr")
        logging.debug(f"{self.qsfp_name} lowpwr: {qsfp_reg}")

    def read_qsfp_low_power_mode_reg(self):
        # 1'b0: module is not in low-power mode 
        # 1'b1: laser and receiver disabled, but I2C is accessable
        qsfp_reg = self.qsfp.read_field("lowpwr")
        return qsfp_reg

    def read_qsfp_mod_prs_n_reg(self):
        # 1'b0: QSFP module is present 
        # 1'b1: QSFP module is not present
        qsfp_reg = not self.qsfp.read_field("mod_prs_n")
        logging.debug(f"{self.qsfp_name} mod_prs_n: {qsfp_reg}")
        return qsfp_reg

    def read_qsfp_interrupt_n_reg(self):
        # When read as '0' this field indicates that the module has a pending 
        # interrupt that can be serviced through the 2-wire serial interface.
        qsfp_reg = self.qsfp.read_field("interrupt_n")
        logging.debug(f"{self.qsfp_name} interrupt_n: {qsfp_reg}")
        return qsfp_reg



def eth_100G_config(Eth_100G_IP_cores, loopback_mode, regsets, checker):
    """Configure the applicable modules within each of the FPGA 100G Ethernet instances
       1. Tranceiver PHY
       2. Tx/Rx statistics 
       3. Reed-Solomon Foward Error Correction"""
    for idx in Eth_100G_IP_cores:
        eth_port_list = idx.get("Eth_100Gs")

    eth_phy = dict()
    eth_stats = dict()
    eth_fec = dict()
    eth_qsfp = dict()
    for port in eth_port_list:
        eth_phy[f"eth{port}__phy"] = ETH_PHY(regsets, f"eth{port}__phy", checker)
        eth_stats[f"eth{port}__statistics"] = ETH_Statistics(regsets, f"eth{port}__tx_statistics", f"eth{port}__rx_statistics")
        eth_fec[f"eth{port}__rsfec"] = ETH_RSFEC(regsets, f"eth{port}__tx_rsfec", f"eth{port}__rx_rsfec")
        eth_qsfp[f"eth{port}__qsfp"] = ETH_QSFP(regsets, f"eth{port}__qsfp")

    for phy_name, phy in eth_phy.items():
        # logging.info(f"ETH PHY dictionary: key = {phy_name}, value = {phy}")
        phy.check_phy_regs()
        phy.config_phy_link_regs(loopback_mode)
    idx = 0
    for qsfp_name, qsfp in eth_qsfp.items():
        # logging.info(f"ETH QSFP dictionary: key = {qsfp_name}, value = {qsfp}")
        qsfp_present = qsfp.read_qsfp_mod_prs_n_reg()
        checker.check(qsfp_present == True, f"{qsfp.qsfp_name} QSFP module present: {qsfp_present}")
        if (qsfp_present == False and loopback_mode == False):
            qsfp.qsfp_config_valid = False
            logging.info(f"FAILED check. eth{idx} external loopback test configuration valid: {qsfp.qsfp_config_valid}")
            logging.error(f"FAILED check. eth{idx} test cannot be performed, QSFP not connected.")
            qsfp.set_qsfp_low_power_mode(True)
        else:
            qsfp.qsfp_config_valid = True
            logging.info(f"PASSED check. eth{idx} test configuration valid: {qsfp.qsfp_config_valid}")
            logging.info(f"PASSED check. eth{idx} test will be performed.")
            if loopback_mode == True:
                qsfp.set_qsfp_low_power_mode(True)
        idx += 1
    for fec_name, fec in eth_fec.items():
        # logging.info(f"ETH FEC dictionary: key = {fec_name}, value = {fec}")
        fec.config_fec_regs()
    for stats_name, stats in eth_stats.items():
        # logging.info(f"ETH STATS dictionary: key = {stats_name}, value = {stats}")
        stats.config_stats_regs()
    for fec_name, fec in eth_fec.items():
        fec.insert_fec_errors()

    return [eth_phy, eth_stats, eth_fec, eth_qsfp]

def eth_100G_error_test(eth_phy, eth_stats, eth_fec, eth_qsfp, Eth_100G_IP_cores, runtime, rx_loopback_mode,checker, current_time):
    """100G Ethernet
       Checks if the received Reed-Solomon FEC codewords are corrected and display
       a summary of the various Ethernet parameters checked in tabular format."""
    if not rx_loopback_mode:
        logging.info(f"100G Ethernet test external loopback mode [using loopback cable]")
    else:
        logging.info(f"100G Ethernet test internal loopback mode [using XCVR PHY Rx serial loopback]")

    for idx in Eth_100G_IP_cores:
        board = idx.get("board")
        eth_port_list = idx.get("Eth_100Gs")
    
    READ_TIME_SEC = 10.0  # arbitrary value to read counters before they saturate
    bert_cntr = runtime
    
    if (runtime % READ_TIME_SEC) == 0:  
        additional_loops = 1
    else:
        additional_loops = 2
    LOOP_CNT = int(runtime / READ_TIME_SEC) + additional_loops
    
    start = time.time()
    est_time = runtime
    logging.info(f"Ethernet error check test will take approximately {est_time:1.1f} seconds ...")

    with tqdm.tqdm(total=est_time) as pbar:
        for lc in range(0, LOOP_CNT, 1):
            for fec_name, fec in eth_fec.items():
                fec.rx_fec_corr_cw_cntr = fec.rx_fec_corr_cw_cntr + fec.read_fec_rx_corr_cw_cntr_reg()
                fec.rx_fec_uncorr_cw_cntr = fec.rx_fec_uncorr_cw_cntr + fec.read_fec_rx_uncorr_cw_cntr_reg()
                # clear any residual errors after the first pass
                if lc == 0:
                    fec.rx_fec_corr_cw_cntr = 0
                    fec.rx_fec_uncorr_cw_cntr = 0
                # check error count
                if lc == (LOOP_CNT - 1):
                    if fec.read_fec_tx_error_insertion_all_reg():
                        fec_tx_error_ins = True
                        checker.check(
                            ((fec.rx_fec_corr_cw_cntr != 0.0) and (fec.rx_fec_uncorr_cw_cntr == 0.0)), 
                            f"{fec_name} 100G Ethernet Rx FEC: corrected codewords = {fec.rx_fec_corr_cw_cntr}, uncorrected codewords = {fec.rx_fec_uncorr_cw_cntr}",
                            # True
                            )
                    else:
                        fec_tx_error_ins = False
                        checker.check(
                            ((fec.rx_fec_corr_cw_cntr == 0.0) and (fec.rx_fec_uncorr_cw_cntr == 0.0)), 
                            f"{fec_name} 100G Ethernet Rx FEC: corrected codewords = {fec.rx_fec_corr_cw_cntr}, uncorrected codewords = {fec.rx_fec_uncorr_cw_cntr}",
                            # True
                            )
            if lc == 0:
                if bert_cntr == 0:
                    break                            
                if bert_cntr <= READ_TIME_SEC:
                    time.sleep(bert_cntr)
                else:
                    bert_cntr = bert_cntr - READ_TIME_SEC
                    time.sleep(READ_TIME_SEC)
            else: 
                if lc < (LOOP_CNT - 1):
                    if bert_cntr <= READ_TIME_SEC:
                        time.sleep(bert_cntr)
                    else:
                        bert_cntr = bert_cntr - READ_TIME_SEC
                        time.sleep(READ_TIME_SEC)
            pbar.update(READ_TIME_SEC)

    end = time.time()
    logging.info(f"100G Ethernet test finished in {end-start:1.1f} seconds.")

    if fec_tx_error_ins:
        logging.info(f"100G Ethernet Test Summary - With Tx FEC Codeword Error Insertion Enabled")
    else:
        logging.info(f"100G Ethernet Test Summary - Without Tx FEC Codeword Error Insertion Enabled")

    influx_csv_writer = bist_utils.influx_csv('bist.csv')
    data_type = ['measurement','tag','string','string','string','string','string','string','string','long','string','long','long','dateTime:RFC3339']
    influx_csv_writer.write_datatype(data_type)

    # Display the 100G Ethernet Core BIST Status
    # Loopback: 0x0 = external, 0xF = Rx serial (internal)
    # Clock Data Recovery (CDR): 0x0 = False, 0xF = True
    # Reed-Solom FEC: Rx corrected and uncorrected codewords
    header_col = [
        "Register",
        "PHY",
        "QSFP pres",
        "QSFP LP mode",
        "Loopback",
        "Wordlock",
        "Freqlock",
        "Frame error",
        "Tx CW errors",
        "Rx FCS error",
        "Rx parity error",
        "Rx Corrected_CW",
        "Rx UnCorrected_CW",
    ]

    table = BeautifulTable(maxwidth=200, precision=32)
    table.columns.header = header_col
    influx_csv_writer.write_header(header_col)
    for port in eth_port_list:
        data_row = ["phy_status"]
        data_row = (
            data_row
            + [f"eth{port}"]
            + [eth_qsfp[f"eth{port}__qsfp"].read_qsfp_mod_prs_n_reg()]
            + [eth_qsfp[f"eth{port}__qsfp"].read_qsfp_low_power_mode_reg()]
            + [hex(eth_phy[f"eth{port}__phy"].read_phy_loopback_reg())]
            + [hex(eth_phy[f"eth{port}__phy"].read_phy_word_lock_reg())]
            + [hex(eth_phy[f"eth{port}__phy"].read_phy_freq_lock_reg())]
            + [hex(eth_phy[f"eth{port}__phy"].read_phy_frame_error_reg())]
            + [eth_fec[f"eth{port}__rsfec"].read_fec_tx_error_insertion_all_reg()]
            + [eth_stats[f"eth{port}__statistics"].read_stats_rx_fcs_cntr_reg()]
            + [eth_stats[f"eth{port}__statistics"].read_stats_rx_parity_err_reg()]
            + [eth_fec[f"eth{port}__rsfec"].rx_fec_corr_cw_cntr]
            + [eth_fec[f"eth{port}__rsfec"].rx_fec_uncorr_cw_cntr]
            )
        table.rows.append(data_row)
        influx_csv_writer.write_csv(data_row, current_time)
    logging.info(table)


def main(Eth_100G_IP_cores, eth_phy_loopback_mode, runtime, regsets, current_time):
    # bist_utils.Date().log_timestamp()
    checker = bist_utils.Checker()
    logging.info(f"#---------------------------------------------------------")
    logging.info(f"Talon-DX FPGA BIST testcase: 100G Ethernet")
    # check the Ethernet PHY link status using RS-FEC codeword correction
    [eth_phy, stats, eth_fec, eth_qsfp] = eth_100G_config(Eth_100G_IP_cores, eth_phy_loopback_mode, regsets, checker)
    eth_100G_error_test(eth_phy, stats, eth_fec, eth_qsfp, Eth_100G_IP_cores, runtime, eth_phy_loopback_mode, checker, current_time)
    checker.report_log(f"100G Ethernet loopback test results")
    # repeat test without FEC codeword error insertion
    for fec_name, fec in eth_fec.items():
        fec.enable_fec_tx_error_insertion_all(False)
    eth_100G_error_test(eth_phy, stats, eth_fec, eth_qsfp, Eth_100G_IP_cores, runtime, eth_phy_loopback_mode, checker, current_time)
    checker.report_log(f"100G Ethernet loopback test results")
    # disable various test configuration parameters, could be connected to a network:
    for qsfp_name, qsfp in eth_qsfp.items():
        qsfp.set_qsfp_low_power_mode(False)
    for phy_name, phy in eth_phy.items():
        phy.set_phy_loopback(False)
    return checker



if __name__ == "__main__":
    logging.info("tdc_base_bist_ethernet: __main__")
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
        testcase = "100G Ethernet Int_LB",
        Eth_100G_runtime = 1.0,          # test time in seconds
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
        logging.info("Arguments loaded from defaults in script")

    testcase = args.get('testcase')
    assert ((testcase == "100G Ethernet Int_LB") or (testcase == "100G Ethernet Ext_LB")), \
            f"100G Etnernet BIST: {testcase} testcase not found"
    runtime = args.get('Eth_100G_runtime')
    Eth_100G_IP_cores = args.get('Eth_100G_IP_cores') 

    #-------------------------------------------------------------------------
    # FPGA module BIST test:
    #-------------------------------------------------------------------------
    # 100G Ethernet loopback mode: 0 = external, 1 = Rx serial
    if testcase == "100G Ethernet Int_LB":
        eth_phy_loopback_mode = 1
    elif testcase == "100G Ethernet Ext_LB":
            eth_phy_loopback_mode = 0
    else:
        logging.error(f"Invalid testcase {testcase}!")

    checker = main(Eth_100G_IP_cores, eth_phy_loopback_mode, runtime, regsets)    