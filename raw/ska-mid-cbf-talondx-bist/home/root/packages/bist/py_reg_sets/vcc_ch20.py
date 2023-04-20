from register_access import pyField, RegFile

class vcc_ch20_regs(RegFile):
    _version = "1.00"
    _size = 84
    _fields = {
        "frame_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=220000000),
        "fs_sft" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x04, reg_repeat=  20, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=2),
        "fs_scl" :
            pyField( offset= 4, ftype='natural', width=16, repeat=   1, reg_offset=0x04, reg_repeat=  20, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=62094),
        }