from register_access import pyField, RegFile

class gaussian_regs(RegFile):
    _version = "1.0"
    _size = 20
    _fields = {
        "magic_number" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "revision" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "seed_ln" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "seed_cos" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "mean" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "std" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        }