from register_access import pyField, RegFile

class Ethernet_100G_tx_statistics_regs(RegFile):
    _version = "19.2.0"
    _size = 400
    _fields = {
        "cntr_tx_fragments" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_jabbers" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_fcs" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_crcerr" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_mcast_data_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_bcast_data_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_ucast_data_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x30, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_mcast_ctrl_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x38, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_bcast_ctrl_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_ucast_ctrl_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_pause_err" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x50, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_64b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x58, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_65to127b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x60, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_128to255b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x68, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_256to511b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x70, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_512to1023b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x78, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_1024to1518b" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x80, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_1519tomaxb" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x88, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_oversize" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x90, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_mcast_data_ok" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x98, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_bcast_data_ok" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xA0, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_ucast_data_ok" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xA8, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_mcast_ctrl" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xB0, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_bcast_ctrl" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xB8, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_ucast_ctrl" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xC0, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_pause" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xC8, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "cntr_tx_runt" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0xD0, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "tx_cnt_clr" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x114, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "tx_parity_err_clr" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x114, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "tx_shadow_req" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x114, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "tx_parity_err" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x118, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "tx_cnt_pause" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x118, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "txpayloadoctetsok" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x180, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "txframeoctetsok" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x188, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        }