from register_access import pyField, RegFile

class first_order_delay_models_regs(RegFile):
    _version = "1.0"
    _size = 32768
    _fields = {
        "first_input_timestamp" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 8, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "delay_constant" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "delay_linear" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=1073741824),
        "phase_constant" :
            pyField( offset= 0, ftype='integer', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "phase_linear" :
            pyField( offset= 0, ftype='integer', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "validity_period" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "output_PPS" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        "first_output_timestamp" :
            pyField( offset= 0, ftype='natural', width=64, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 8, set_repeat= 512, set_byte_width=64, readable=True, writeable=True, reset=0),
        }