from register_access import pyField, RegFile

class ic_ch16k_regs(RegFile):
    _version = "1.00"
    _size = 131072
    _fields = {
        "ic_sft" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=32768, set_byte_width= 4, readable=True, writeable=True, reset=7),
        "ic_scl" :
            pyField( offset= 4, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=32768, set_byte_width= 4, readable=True, writeable=True, reset=65535),
        }