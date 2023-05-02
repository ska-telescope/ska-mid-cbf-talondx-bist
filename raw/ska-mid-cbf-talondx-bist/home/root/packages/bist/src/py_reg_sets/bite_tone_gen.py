from register_access import pyField, RegFile

class bite_tone_gen_regs(RegFile):
    _version = "1.00"
    _size = 8
    _fields = {
        "phase_inc" :
            pyField( offset= 0, ftype='integer', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=True, reset=0),
        "mag_scale" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=True, reset=0),
        }