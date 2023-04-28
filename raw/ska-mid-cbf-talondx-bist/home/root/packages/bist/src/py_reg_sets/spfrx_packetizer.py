from register_access import pyField, RegFile

class spfrx_packetizer_regs(RegFile):
    _version = "0.1.0"
    _size = 112
    _fields = {
        "id" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=1811366569),
        "version" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=65536),
        "sw_rst" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=1),
        "sf_fifo_ovf" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "metafifo_ovf" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "loc_mac_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=4386),
        "loc_mac_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=860116326),
        "rem_mac_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=30600),
        "rem_mac_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=2578103244),
        "ethertype" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=65261),
        "dish_id" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "hw_src_id_h" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "hw_src_id_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x2C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band12_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x30, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band12_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x34, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band3_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x38, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band3_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x3C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band45b_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x40, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band45b_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x44, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band5a_h" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "sample_rate_band5a_l" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x4C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "gpi" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x50, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "gpo" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x54, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band1_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x58, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band1_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x58, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band2_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x5C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band2_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x5C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band3_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x60, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band3_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x60, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band4_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x64, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band4_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x64, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band5a_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x68, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band5a_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x68, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band5b_holdoff_rise" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x6C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "band5b_holdoff_fall" :
            pyField( offset=16, ftype='natural', width=16, repeat=   1, reg_offset=0x6C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        }