from register_access import pyField, RegFile

class vcc_ch20_org_regs(RegFile):
    _version = "1.00"
    _size = 128
    _fields = {
        "flg_ext" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=36),
        "frame_count" :
            pyField( offset= 0, ftype='integer', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=220000000),
        "fs_ms_p0" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x08, reg_repeat=  10, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=65536),
        "fs_ms_p1" :
            pyField( offset=16, ftype='integer', width=16, repeat=   1, reg_offset=0x08, reg_repeat=  10, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=1),
        "fs_mc_p0" :
            pyField( offset= 0, ftype='integer', width=18, repeat=   1, reg_offset=0x30, reg_repeat=  10, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=65536),
        "fs_mc_p1" :
            pyField( offset= 0, ftype='integer', width=18, repeat=   1, reg_offset=0x58, reg_repeat=  10, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=65536),
        }