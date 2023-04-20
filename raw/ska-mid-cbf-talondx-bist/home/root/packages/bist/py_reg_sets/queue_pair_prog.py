from register_access import pyField, RegFile

class queue_pair_prog_regs(RegFile):
    _version = "1.0"
    _size = 28
    _fields = {
        "mac_addr_high" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "mac_addr_low" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "ip_address" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "p_key" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "dest_QP" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "PSN" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        "queue_id" :
            pyField( offset= 0, ftype='natural', width=10, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=False, writeable=True, reset=0),
        }