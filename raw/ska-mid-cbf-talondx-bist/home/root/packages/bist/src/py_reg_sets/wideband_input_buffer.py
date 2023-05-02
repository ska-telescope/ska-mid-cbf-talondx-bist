from register_access import pyField, RegFile

class wideband_input_buffer_regs(RegFile):
    _version = "1.2.0"
    _size = 72
    _fields = {
        "receive_enable" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "packet_error" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "packet_drop" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "link_failure" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "buffer_overflow" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "firmware_band" :
            pyField( offset= 0, ftype='natural', width= 4, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "stream_rate" :
            pyField( offset= 0, ftype='natural', width=28, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "packet_rate" :
            pyField( offset= 0, ftype='natural', width= 9, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "noise_diode_transition_holdoff_count" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "packet_error_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "packet_drop_count" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "los_seconds" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_ethertype" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x24, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_dish_id" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_band_id" :
            pyField( offset=16, ftype='natural', width= 8, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_utc_time_code" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x2C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_transport_sample_rate_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x30, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_transport_sample_rate_msw" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x34, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_hardware_source_id_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x38, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "meta_hardware_source_id_msw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x3C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "rx_packet_rate" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "rx_sample_rate" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x44, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        }