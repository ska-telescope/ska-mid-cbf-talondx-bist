from register_access import pyField, RegFile

class subarray_spead_descriptors_regs(RegFile):
    _version = "1.0"
    _size = 512
    _fields = {
        "channel_id" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        "channel_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=1),
        "baseline_id" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        "baseline_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        "scan_id_high" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        "scan_id_low" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        "visibility_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=  16, set_byte_width=32, readable=True, writeable=True, reset=0),
        }