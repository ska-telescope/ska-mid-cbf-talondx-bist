from register_access import pyField, RegFile

class polarization_coupler_regs(RegFile):
    _version = "1.00"
    _size = 12
    _fields = {
        "delay_enable" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "alpha" :
            pyField( offset= 0, ftype='integer', width=18, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "beta" :
            pyField( offset= 0, ftype='integer', width=18, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=65536),
        }