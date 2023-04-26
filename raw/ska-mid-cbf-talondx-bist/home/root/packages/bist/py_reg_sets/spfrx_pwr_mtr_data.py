from register_access import pyField, RegFile

class spfrx_pwr_mtr_data_regs(RegFile):
    _version = "1.00"
    _size = 4096
    _fields = {
        "data" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=1024, set_byte_width= 4, readable=True, writeable=False, reset=0),
        }