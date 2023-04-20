from register_access import pyField, RegFile

class talon_status_regs(RegFile):
    _version = "1.00"
    _size = 112
    _fields = {
        "system_clk_fault" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "iopll_locked_fault" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "fs_iopll_locked_fault" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "comms_iopll_locked_fault" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_bl_fault" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_br_fault" :
            pyField( offset= 5, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_tr_fault" :
            pyField( offset= 6, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_0_pll_fault" :
            pyField( offset= 7, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_1_pll_fault" :
            pyField( offset= 8, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_fault" :
            pyField( offset= 9, ftype='boolean', width= 1, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "non_zero" :
            pyField( offset=10, ftype='natural', width= 6, repeat=   1, reg_offset=0x00, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "base_clock_frequency" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x04, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_bl_clock_frequency" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x0C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_br_clock_frequency" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x10, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_tr_clock_frequency" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x14, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "iopll_locked" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "fs_iopll_locked" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "comms_iopll_locked" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x18, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "iopll_locked_trn" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "fs_iopll_locked_trn" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "comms_iopll_locked_trn" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x1C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_pll_locked" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_local_reset_done" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_local_cal_success" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_local_cal_fail" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_amm_ready" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "emif_reset" :
            pyField( offset= 5, ftype='boolean', width= 1, repeat=   1, reg_offset=0x20, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_pll_locked_trn" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_local_reset_done_trn" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_local_cal_success_trn" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_local_cal_fail_trn" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "emif_amm_ready_trn" :
            pyField( offset= 4, ftype='boolean', width= 1, repeat=   1, reg_offset=0x2C, reg_repeat=   3, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "e100g_main_pll_locked" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x38, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_main_pll_cal_busy" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x38, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_buffer_pll_locked" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x38, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_buffer_pll_cal_busy" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x38, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "e100g_main_pll_locked_trn" :
            pyField( offset= 0, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "e100g_main_pll_cal_busy_trn" :
            pyField( offset= 1, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "e100g_buffer_pll_locked_trn" :
            pyField( offset= 2, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "e100g_buffer_pll_cal_busy_trn" :
            pyField( offset= 3, ftype='boolean', width= 1, repeat=   1, reg_offset=0x40, reg_repeat=   2, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "slim_is_present_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x48, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_is_present_msw" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x4C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_locked_status_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x50, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_locked_status_msw" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x54, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_locked_status_trn_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x58, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "slim_pll_locked_status_trn_msw" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x5C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "slim_pll_cal_busy_status_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x60, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_cal_busy_status_msw" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x64, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=False, reset=0),
        "slim_pll_cal_busy_status_trn_lsw" :
            pyField( offset= 0, ftype='natural', width=32, repeat=   1, reg_offset=0x68, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        "slim_pll_cal_busy_status_trn_msw" :
            pyField( offset= 0, ftype='natural', width=24, repeat=   1, reg_offset=0x6C, reg_repeat=   1, reg_byte_width= 4, set_repeat=   1, set_byte_width=128, readable=True, writeable=True, reset=0),
        }