from register_access import pyField, RegFile

class lstv_replay_regs(RegFile):
    _version = "2.0"
    _size = 40
    _fields = {
        "sample_rate" :
            pyField( offset= 0, ftype='natural', width=33, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=3963617280),
        "ref_clk_freq" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "run" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "lstv_current_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "lstv_start_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "lstv_end_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "samples_per_cycle" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "start_utc_time_code" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        }