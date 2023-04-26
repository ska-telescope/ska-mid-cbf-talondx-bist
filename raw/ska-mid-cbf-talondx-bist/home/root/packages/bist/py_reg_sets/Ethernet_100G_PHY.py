from register_access import pyField, RegFile

class Ethernet_100G_PHY_regs(RegFile):
    _version = "19.2.1"
    _size = 324
    _fields = {
        "REVID" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "scratch" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "phy_name_0" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "phy_name_1" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "phy_name_2" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "eio_sys_rst" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "soft_txp_rst" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "soft_rxp_rst" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "set_ref_lock" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "set_data_lock" :
            pyField( offset= 5, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "word_lock" :
            pyField( offset= 0, ftype='natural', width=20, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "eio_sloop" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x4C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "eio_flag_sel" :
            pyField( offset= 0, ftype='natural', width= 3, repeat=   1, reg_offset=0x50, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "eio_flags" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x54, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "eio_freq_lock" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x84, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "tx_reset_done" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x88, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "tx_core_clock_stable" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x88, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "rx_core_clock_stable" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x88, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "frm_err" :
            pyField( offset= 0, ftype='natural', width=20, repeat=   1, reg_offset=0x8C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "sclr_frm_err" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x90, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "clear_rx_fifo" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x94, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "disable_bitslip" :
            pyField( offset=11, ftype='boolean', width= 1, repeat=   1, reg_offset=0x94, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "disable_autoadaption" :
            pyField( offset=12, ftype='boolean', width= 1, repeat=   1, reg_offset=0x94, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "rx_pcs_fully_aligned" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x98, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "RX_PCS_HI_BER" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x98, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "err_inj" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x9C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "am_lock" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0xA0, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "all_lanes_deskewed" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0xA4, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "deskew_change" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0xA4, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "vlane_a" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   5, reg_offset=0xC0, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "vlane_b" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   5, reg_offset=0xC4, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "vlane_c" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   5, reg_offset=0xC8, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "vlane_d" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   5, reg_offset=0xCC, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "khz_ref" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x100, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "khz_rx" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x104, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "khz_tx" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x108, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "khz_tx_rs" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "khz_rx_rs" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x110, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "enable_rsfec" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x140, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        }