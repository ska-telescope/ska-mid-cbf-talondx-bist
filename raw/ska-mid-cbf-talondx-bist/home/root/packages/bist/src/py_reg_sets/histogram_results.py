from register_access import pyField, RegFile

class histogram_results_regs(RegFile):
    _version = "1.00"
    _size = 32768
    _fields = {
        "bin" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=8192, set_byte_width= 4, readable=True, writeable=False, reset=0),
        }