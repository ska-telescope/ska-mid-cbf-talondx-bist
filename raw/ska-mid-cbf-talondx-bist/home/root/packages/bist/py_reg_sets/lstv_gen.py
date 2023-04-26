from register_access import pyField, RegFile

class lstv_gen_regs(RegFile):
    _version = "2.1"
    _size = 80
    _fields = {
        "magic_number" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "revision" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "ip_control" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "ip_status" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "memory_ready" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "ddr4_current_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "ddr4_start_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "ddr4_end_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "tone_select" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "source_select" :
            pyField( offset= 4, ftype='natural', width= 4, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "receiver_select" :
            pyField( offset= 8, ftype='boolean', width= 1, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "source_mean_polX" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x20, reg_repeat=   4, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "source_mean_polY" :
            pyField( offset=16, ftype='integer', width=16, repeat=   1, reg_offset=0x20, reg_repeat=   4, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "source_std_polX" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x30, reg_repeat=   4, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "source_std_polY" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x30, reg_repeat=   4, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "receiver_mean_polX" :
            pyField( offset= 0, ftype='integer', width=16, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "receiver_mean_polY" :
            pyField( offset=16, ftype='integer', width=16, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "receiver_std_polX" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x44, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "receiver_std_polY" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x44, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "low_address_allocation" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "high_address_allocation" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x4C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        }