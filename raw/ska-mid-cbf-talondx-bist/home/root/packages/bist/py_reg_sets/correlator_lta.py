from register_access import pyField, RegFile

class correlator_lta_regs(RegFile):
    _version = "1.0"
    _size = 16
    _fields = {
        "set_active_bank" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "current_active_bank" :
            pyField( offset= 4, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "num_banks" :
            pyField( offset= 8, ftype='natural', width= 4, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=2),
        "fifo_baselines_to_full" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=False, reset=0),
        "sub_address" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "channel" :
            pyField( offset=16, ftype='natural', width=12, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "bank" :
            pyField( offset=28, ftype='natural', width= 4, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=1),
        "active" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "integration_multiple" :
            pyField( offset= 8, ftype='natural', width= 8, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=1),
        "sub_array" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "channel_ave" :
            pyField( offset=24, ftype='natural', width= 8, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=1),
        "baseline" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        }