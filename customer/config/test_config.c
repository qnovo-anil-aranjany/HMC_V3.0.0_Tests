/**********************************************************************
 * This file is to allow source code to compile for testing purposes.
 **********************************************************************/

#ifdef UNITTEST

/************************************************
 * Include Header Files
 ************************************************/
#include <math.h>

#include "test_config.h"
#include "qnovo_afc_api.h"


/************************************************
 * Global Variables: Mock Inputs from Customers
 ************************************************/
t_uint32            VaAPI_Cmp_NVMRegion[NVM_ARRAY_SIZE];
t_uint8             VaAPI_Cmp_NVMLoggingRegion[NVM_LOGGING__BYTE_SIZE];
t_I_milliamp        VeAPI_I_PackCurr;
t_bool              VeAPI_b_PackCurr_DR;
t_U_millivolt_cell  VaAPI_U_CellVolts[MAX_NUM_CELLS];
t_bool              VaAPI_b_CellVolts_DR[MAX_NUM_CELLS];
t_T_celsius         VaAPI_T_TempSnsrs[MAX_NUM_TEMP_SNSRS];
t_bool              VaAPI_b_TempSnsrs_DR[MAX_NUM_TEMP_SNSRS];
t_T_celsius         VeAPI_T_MinTempSnsr;
t_bool              VeAPI_b_MinTempSnsr_DR;
t_T_celsius         VeAPI_T_MaxTempSnsr;
t_bool              VeAPI_b_MaxTempSnsr_DR;
t_Cap_milliamphr    VeAPI_Cap_ChgPackCapcty;
t_bool              VeAPI_b_ChgPackCapcty_DR;
t_Pct_percent       VeAPI_Pct_PackSOC;
t_bool              VeAPI_b_PackSOC_DR;
t_bool              VeAPI_b_EVSEChgStatus;
t_int32             VeAPI_e_EVSEChgLevel;

/* Transient Output */
t_uint8	VaAFC_Cmp_CTE_Info[CTE_INFO_ARRAY_SIZE];

/* Outputs to Customers */
t_uint32            VeAFC_e_ErrorFlags;
t_I_milliamp_chg    VeAFC_I_ChgPackCurr;
t_U_millivolt_pack  VeAFC_U_ChgPackVolt;
t_bool              VeAFC_b_ChgCompletionFlag;
t_I_milliamp_chg    VeAFC_I_MaxReferenceCurr;
t_I_milliamp_chg 	VeAFC_I_MitigatedCurr;
t_bool              VeAFC_b_ExtremeAgingFlag;
t_bool              VeAFC_b_AbnormalAgingFlag;
t_bool              VeAFC_b_EarlyWarningAgingFlag;
t_bool              VeAFC_b_EOLFlag;
t_bool              VeAFC_b_SOCImbalanceFlag;
t_bool              Output_SlicingStatus;

/* Get functions to test versioning */
t_uint32 get_afc_sw_ver(void);

t_U_millivolt_cell  cell_volts_temp[192];
LIB_CircBuffHandle_t Input_CircBuffHandle_t;
t_uint8*             ele_addr;

/* Obfuscation */
t_int32 VeAPI_Cmp_LogSrc;
t_uint32 VeAPI_Cmp_LogSrcSize = sizeof(VeAPI_Cmp_LogSrc);
t_int32 VeAPI_Cmp_LogDst;

t_int32 VeAPI_Cmp_LogSrcArray[15];
t_uint32 VeAPI_Cmp_LogSrcArraySize = sizeof(VeAPI_Cmp_LogSrcArray);
t_int32 VeAPI_Cmp_LogDstArray[15];
t_U_millivolt_cell  cell_volts_temp[192];
t_U_millivolt_cell  test_cell_ids[5];
LIB_CircBuffHandle_t Input_CircBuffHandle_t;
t_uint8*             ele_addr;

CTE_ESTIMATES_T cte_estimates;
t_uint32 cte_status;


t_uint32 get_afc_sw_ver(void) {
    return QnovoAFC_SW_Version;
}

t_float32 standard_expf(t_float32 x) {
    return expf(x);
}

AFC_INFO_T afc_cte_info;


// lib_utils
/************************************************
 * Global Variables: Mock Inputs from Customers
 ************************************************/
t_Pct_percent VeAPI_Pct_PackSOC;

Point pstruct_1;
Point pstruct_2;

LIB_CircBuffHandle_t Input_CircBuffHandle_t;
t_uint8              buff[10][10];
t_uint8              ele_arr[2];
t_int8               ele_arr_char[2];
t_uint8              ele_arr_overflow_1[2];
t_uint8              ele_arr_overflow_2[2];
t_bool*              is_buff_full;
t_bool*              is_buff_empty;
t_uint16*            num_elements_inserted;
t_int16              ele_index;
t_uint8*             ele_addr_buff;
t_int16              buff_ptr[5];
t_uint16             buffer_entry[10];

#else
#endif

int main(void) {


  return 0;
}
