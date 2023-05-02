from register_access import pyField, RegFile

class bite_fir_filter_regs(RegFile):
    _version = "2.00"
    _size = 4096
    _fields = {
        "filter_coeff" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=1024, set_byte_width= 4, readable=False, writeable=True, reset=0),
        }