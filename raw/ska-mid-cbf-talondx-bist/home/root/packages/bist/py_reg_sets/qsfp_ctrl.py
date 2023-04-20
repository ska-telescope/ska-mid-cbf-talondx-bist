from register_access import pyField, RegFile

class qsfp_ctrl_regs(RegFile):
    _version = "1.00"
    _size = 8
    _fields = {
        "mod_sel_n" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=True, reset=1),
        "reset_n" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=True, reset=1),
        "lowpwr" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=True, reset=0),
        "mod_prs_n" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=False, reset=0),
        "interrupt_n" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width= 8, readable=True, writeable=False, reset=0),
        }