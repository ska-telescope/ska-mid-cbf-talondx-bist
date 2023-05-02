from register_access import pyField, RegFile

class source_host_config_regs(RegFile):
    _version = "1.0"
    _size = 16
    _fields = {
        "mac_addr_high" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "udp_port_offset" :
            pyField( offset=16, ftype='integer', width=16, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "mac_addr_low" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "ip_addr" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x08, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=0),
        "dest_udp_port" :
            pyField( offset= 0, ftype='natural', width=16, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=16, readable=True, writeable=True, reset=4791),
        }