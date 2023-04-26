from register_access import pyField, RegFile

class host_lut_s1_regs(RegFile):
    _version = "1.0"
    _size = 8
    _fields = {
        "channel" :
            pyField( offset= 0, ftype='natural', width=10, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=False, writeable=True, reset=0),
        "subarray" :
            pyField( offset=16, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=False, writeable=True, reset=0),
        "host_id" :
            pyField( offset= 0, ftype='natural', width=10, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=False, writeable=True, reset=0),
        }