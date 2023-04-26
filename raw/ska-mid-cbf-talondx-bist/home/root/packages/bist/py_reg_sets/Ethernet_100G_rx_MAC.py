from register_access import pyField, RegFile

class Ethernet_100G_rx_MAC_regs(RegFile):
    _version = "19.2.0"
    _size = 44
    _fields = {
        "rxmac_revid" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "rxmac_scratch" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "rxmac_name_0" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "rxmac_name_1" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "rxmac_name_2" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "rxmac_size_config" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=9600),
        "mac_crc_config" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "link_fault" :
            pyField( offset= 0, ftype='natural', width= 2, repeat=   1, reg_offset=0x20, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=False, reset=0),
        "rx_vlan_detect_disable" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=0),
        "sfd_check" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=1),
        "preamble_check" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x28, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=64, readable=True, writeable=True, reset=1),
        }