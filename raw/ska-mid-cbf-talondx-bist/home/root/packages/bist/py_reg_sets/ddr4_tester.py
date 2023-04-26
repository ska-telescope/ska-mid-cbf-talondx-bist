from register_access import pyField, RegFile

class ddr4_tester_regs(RegFile):
    _version = "1.00"
    _size = 76
    _fields = {
        "ver_id" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "reset" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "pattern_sel" :
            pyField( offset= 0, ftype='natural', width= 2, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "status" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "err_cnt" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "err_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "block_test_enable" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "spot_addr_coarse" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "spot_addr_fine" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "spot_write_data" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "spot_rw" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "spot_read_data" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x2C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "chk_status" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x30, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "chk_start" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x34, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "chk_done" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x38, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "wr_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x3C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "rd_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "start_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x44, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "stop_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        }