from register_access import pyField, RegFile

class pkt_gen_regs(RegFile):
    _version = "1.1"
    _size = 48
    _fields = {
        "uuid" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "resets" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=15),
        "data_src_sel" :
            pyField( offset= 0, ftype='natural', width= 2, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "sstv_size" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=395),
        "sample_rate" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=1980000000),
        "packet_spacing_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "packet_spacing_hi" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "ref_clk_freq_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "ref_clk_freq_hi" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "inject_error" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "inject_status" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "start_utc_time_code" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x2C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        }