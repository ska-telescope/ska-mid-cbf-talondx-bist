from register_access import pyField, RegFile

class circuit_switch_regs(RegFile):
    _version = "1.0"
    _size = 264
    _fields = {
        "number_of_inputs" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "number_of_outputs" :
            pyField( offset= 8, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=False, reset=0),
        "switch_all" :
            pyField( offset= 0, ftype='natural', width= 2, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        "input_select" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   1, reg_offset=0x08, reg_repeat=  32, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=31),
        "switch_cmd" :
            pyField( offset= 0, ftype='natural', width= 2, repeat=   1, reg_offset=0x88, reg_repeat=  32, reg_byte_width= 4, set_repeat=   1, set_byte_width=512, readable=True, writeable=True, reset=0),
        }