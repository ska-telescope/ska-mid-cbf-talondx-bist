from register_access import pyField, RegFile

class sys_id_regs(RegFile):
    _version = "6e4166c313"
    _size = 16
    _fields = {
        "bitstream" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "prerelease" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "patch" :
            pyField( offset= 8, ftype='natural', width= 8, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "minor" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "major" :
            pyField( offset=24, ftype='natural', width= 8, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "commit" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "scratch" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        }