from register_access import pyField, RegFile

class rx_slim_regs(RegFile):
    _version = "1.0"
    _size = 48
    _fields = {
        "cdr_locked" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "cdr_lost" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "block_aligned" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "block_lost" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "sup_user_idle" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "phy_reset" :
            pyField( offset= 5, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "serial_loopback_enable" :
            pyField( offset= 6, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=1),
        "xcvr_rate" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "counter_width" :
            pyField( offset=24, ftype='natural', width= 6, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "clear_counters" :
            pyField( offset=30, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "latch_counters" :
            pyField( offset=31, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "idle_ctrl_word" :
            pyField( offset= 0, ftype='natural', width=56, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "word_count" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "packet_count" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "idle_count" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "idle_error_count" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        }