from register_access import pyField, RegFile

class correlator_mta_regs(RegFile):
    _version = "1.0"
    _size = 65536
    _fields = {
        "channel_average" :
            pyField( offset= 0, ftype='natural', width= 3, repeat=  20, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 8, set_repeat=8192, set_byte_width= 8, readable=False, writeable=True, reset=0),
        }