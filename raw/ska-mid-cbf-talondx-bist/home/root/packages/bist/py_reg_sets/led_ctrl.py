from register_access import pyField, RegFile

class led_ctrl_regs(RegFile):
    _version = "0.1.0"
    _size = 4
    _fields = {
        "led" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=  32, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 4, readable=True, writeable=True, reset=0),
        }