from register_access import pyField, RegFile

class stream_tpg_regs(RegFile):
    _version = "1.0"
    _size = 24
    _fields = {
        "pattern_select" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "start_im" :
            pyField( offset= 0, ftype='integer', width= 9, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "start_re" :
            pyField( offset=16, ftype='integer', width= 9, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "drop_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "drop_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "recover_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "recover_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        }