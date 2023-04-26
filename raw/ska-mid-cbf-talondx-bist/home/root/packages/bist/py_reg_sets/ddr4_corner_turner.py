from register_access import pyField, RegFile

class ddr4_corner_turner_regs(RegFile):
    _version = "1.1"
    _size = 140
    _fields = {
        "number_of_inputs" :
            pyField( offset= 0, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "number_of_channels" :
            pyField( offset= 8, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "number_of_samples" :
            pyField( offset=24, ftype='natural', width= 8, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "num_sample_groups" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "cell_size" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "iteration_length" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "start_read_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "start_read_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "start_sample_group_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "read_threshold" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "read_timeout_threshold" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "antenna_status" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "under_run_status" :
            pyField( offset= 5, ftype='natural', width= 5, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "read_status" :
            pyField( offset=10, ftype='boolean', width= 1, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "read_timeout_status" :
            pyField( offset=11, ftype='boolean', width= 1, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "clear_under_run_status" :
            pyField( offset= 0, ftype='natural', width= 5, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "clear_read_timeout_status" :
            pyField( offset= 5, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "snapshot_timestamps" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        "write_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x30, reg_repeat=   5, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "write_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x44, reg_repeat=   5, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "read_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x58, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "read_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x5C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "first_write_timestamp_lo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x60, reg_repeat=   5, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "first_write_timestamp_hi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x74, reg_repeat=   5, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=False, reset=0),
        "corner_turner_reset" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x88, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=256, readable=True, writeable=True, reset=0),
        }