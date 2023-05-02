from register_access import pyField, RegFile

class fw_debugger_regs(RegFile):
    _version = "1.0"
    _size = 128
    _fields = {
        "debug_register" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=  32, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        }