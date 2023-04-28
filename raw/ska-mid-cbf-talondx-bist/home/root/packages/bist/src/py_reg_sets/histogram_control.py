from register_access import pyField, RegFile

class histogram_control_regs(RegFile):
    _version = "1.00"
    _size = 12
    _fields = {
        "clear" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "start" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "stop" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "done" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "LOG2_NUM_BINS" :
            pyField( offset= 8, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "LOG2_MAX_COUNT" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "channel" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "samples_between_pps" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        }