from register_access import pyField, RegFile

class sstv_regs(RegFile):
    _version = "1.00"
    _size = 65536
    _fields = {
        "sstv" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 8, set_repeat=8192, set_byte_width= 8, readable=True, writeable=True, reset=0),
        }