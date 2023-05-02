from register_access import pyField, RegFile

class resampler_delay_tracker_regs(RegFile):
    _version = "1.1"
    _size = 24
    _fields = {
        "run" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "enable_resampler_dithering" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=1),
        "enable_phase_correction_dithering" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=1),
        "timestamp_gap_detected" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=1),
        "fodm_buffer_depth" :
            pyField( offset= 4, ftype='natural', width=12, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "input_buffer_depth" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "fodm_read_pointer" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   2, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        "dither_seed_x" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "dither_seed_y" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=32, readable=True, writeable=True, reset=0),
        "input_timestamp" :
            pyField( offset= 0, ftype='integer', width=64, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 8, set_repeat=   1, set_byte_width=32, readable=True, writeable=False, reset=0),
        }