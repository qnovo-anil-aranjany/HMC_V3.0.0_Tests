"""This main test module serves as an indicator for TAF to trigger pytest, executing all test cases in this tst
directory. Additionally, it sets up necessary imports and parameters for other test modules in this 'tst' directory to
leverage."""

import ast
import csv
from os.path import abspath, dirname, join
from pathlib import Path

import cffi
import numpy as np
import pytest
import random
from pytest import fixture, mark, param
from src.common import (
    PROJECT_PATH,
    clean_dat_files,
    compare_result,
    get_lib_callables,
    invoke_pytest,
    lib,
    lib_array_to_list,
    log_stack_parametrized_inputs,
    parametrize_args,
    read_json_results,
    record_test_data,
    set_lib_inputs,
    size,
    validate_test_cases,
    write_json_results,
)

MAKE_HTML = True  # Set true to allow html report generation.

ffi = cffi.FFI()

_MODULE_PATH = abspath(__file__)
_TIME_BASED_INPUT_DATA = "test_data\\time_based_data\\input_data"
_TIME_BASED_OUTPUT_DATA = "test_data\\time_based_data\\output_data"
_TIME_BASED_REFERENCE_DATA = "test_data\\time_based_data\\reference_data"
_TOTAL_BYTES = 18


@fixture(scope="function")
def setup_parameters(lib) -> None:
    """This fixture initializes the global variables in the specified library module at the beginning of each test
    function. These variables are reset to their initial values for every standard and parametrized test case, ensuring
    consistent test conditions.

    Args:
        lib (module): The shared library module, either a .dll (Windows) or .so (Unix/Linux) file, containing the global
         variables to be initialized.
    """

    # Data Ready Signals
    # ------------------------------------------------
    lib.VeAPI_b_PackCurr_DR = 1
    lib.VaAPI_b_CellVolts_DR = [1] * size(lib.VaAPI_b_CellVolts_DR)
    lib.VaAPI_b_TempSnsrs_DR = [1] * size(lib.VaAPI_b_TempSnsrs_DR)
    lib.VeAPI_b_MinTempSnsr_DR = 1
    lib.VeAPI_b_MaxTempSnsr_DR = 1
    lib.VeAPI_b_ChgPackCapcty_DR = 1
    lib.VeAPI_b_PackSOC_DR = 1

    # NVM Initialization
    # ------------------------------------------------
    lib.VeAFC_b_ControllerWakeUp = 0
    lib.VeAFC_b_ChargeSessionInit = 0
    lib.VeAPI_b_EVSEChgStatus = 1
    lib.VeAPI_I_PackCurr = 1

    lib.fs_API_SetInputsAFC(
        lib.VaAPI_Cmp_NVMRegion,
        lib.VaAPI_Cmp_NVMLoggingRegion,
        lib.VeAPI_I_PackCurr,
        lib.VeAPI_b_PackCurr_DR,
        lib.VaAPI_U_CellVolts,
        lib.VaAPI_b_CellVolts_DR,
        lib.VaAPI_T_TempSnsrs,
        lib.VaAPI_b_TempSnsrs_DR,
        lib.VeAPI_T_MinTempSnsr,
        lib.VeAPI_b_MinTempSnsr_DR,
        lib.VeAPI_T_MaxTempSnsr,
        lib.VeAPI_b_MaxTempSnsr_DR,
        lib.VeAPI_Cap_ChgPackCapcty,
        lib.VeAPI_b_ChgPackCapcty_DR,
        lib.VeAPI_Pct_PackSOC,
        lib.VeAPI_b_PackSOC_DR,
        lib.VeAPI_b_EVSEChgStatus,
        ffi.addressof(lib, "VaAFC_Cmp_CTE_Info"),
        ffi.addressof(lib, "VeAFC_e_ErrorFlags"),
        ffi.addressof(lib, "VeAFC_I_ChgPackCurr"),
        ffi.addressof(lib, "VeAFC_I_MaxReferenceCurr"),
        ffi.addressof(lib, "VeAFC_I_MitigatedCurr"),
        ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
        ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
        ffi.addressof(lib, "VeAFC_b_ExtremeAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_AbnormalAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_EarlyWarningAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_EOLFlag"),
        ffi.addressof(lib, "VeAFC_b_SOCImbalanceFlag"),
    )
    lib.Qnovo_AFC_Init()
    for i in range(3):
        lib.f_AFC_NVMInit()
    lib.AFC_NVMLoggingInit()
    # Calculation
    # ------------------------------------------------
    lib.s_AFC_Calc.VeAFC_e_QNS_State = 0
    lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum = 0
    lib.s_AFC_Calc.VeAFC_I_CV_Curr = lib.s_AFC_Param.KeAFC_I_CV_ChgCurr
    lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag = [0] * size(
        lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag
    )
    lib.s_AFC_Calc.VaAFC_U_SampleCellVolt = [0] * size(
        lib.s_AFC_Calc.VaAFC_U_SampleCellVolt
    )

    lib.VeAPI_T_MinTempSnsr = 350
    lib.VeAPI_T_MaxTempSnsr = 550

    lib.s_AFC_Calc.VeAFC_T_StdU_RefCellTemp = 350.0 / 10.0
    # Customer Inputs
    # ------------------------------------------------
    lib.KeINP_n_MaxNumCells = 10
    lib.KeINP_n_MaxNumTempSnsrs = 18
    lib.KaINP_i_Temp2CellIdx = [i // 12 for i in range(192)]

    lib.VeAPI_Pct_PackSOC = 5000
    lib.VeAPI_Cap_ChgPackCapcty = 16 * 1000

    random.seed(44)
    noise_mV = [random.uniform(-100, 100) for _ in range(size(lib.VaAPI_U_CellVolts))]
    lib.VaAPI_U_CellVolts = [3200 + int(noise_mV[i]) for i in range(size(lib.VaAPI_U_CellVolts))]

    # lib.VaAPI_U_CellVolts = [3200] * size(lib.VaAPI_U_CellVolts)

    lib.VaAPI_T_TempSnsrs = [-150 + i * 50 for i in range(size(lib.VaAPI_T_TempSnsrs) - 2)]
    lib.VaAPI_T_TempSnsrs[size(lib.VaAPI_T_TempSnsrs) - 2] = min(list(lib.VaAPI_T_TempSnsrs))
    lib.VaAPI_T_TempSnsrs[size(lib.VaAPI_T_TempSnsrs) - 1] = max(list(lib.VaAPI_T_TempSnsrs))

    # lib.VaAPI_T_TempSnsrs = [-100 + i * 50 for i in range(size(lib.VaAPI_T_TempSnsrs))]

    # lib.VaAPI_T_TempSnsrs = [350] * size(lib.VaAPI_T_TempSnsrs)

    lib.VeAPI_I_PackCurr = 50000
    # Customer Outputs
    # ------------------------------------------------
    lib.VeAFC_e_ErrorFlags = 0
    lib.VeAFC_I_ChgPackCurr = 0
    lib.VeAFC_U_ChgPackVolt = 0
    lib.VeAFC_b_ChgCompletionFlag = 0

    # OCV vs. SOC
    # ------------------------------------------------
    lib.KaLIB_U_OCVAxis = [
        3165,
        3277,
        3309,
        3341,
        3354,
        3408,
        3469,
        3504,
        3544,
        3574,
        3592,
        3644,
        3658,
        3672,
        3686,
        3719,
        3762,
        3808,
        3839,
        3861,
        3895,
        3928,
        3955,
        3978,
        4032,
        4058,
        4071,
        4080,
        4101,
        4111,
        4121,
        4142,
        4147,
        4167,
        4195,
        4252,
    ]

    lib.KaLIB_Pct_SOCAxis = [
        0,
        180,
        250,
        340,
        420,
        1000,
        1500,
        1820,
        2250,
        2650,
        2940,
        3950,
        4200,
        4420,
        4610,
        5000,
        5400,
        5750,
        6000,
        6220,
        6610,
        7000,
        7300,
        7530,
        8020,
        8280,
        8440,
        8580,
        9060,
        9240,
        9380,
        9570,
        9600,
        9710,
        9830,
        10000,
    ]

    # NVM
    # ------------------------------------------------
    size_row, size_col = size(lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx)
    lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx = [[0] * size_col for _ in range(size_row)]
    size_row, size_col = size(lib.s_AFC_Track.NtAFC_U_RefCellVolt)
    lib.s_AFC_Track.NtAFC_U_RefCellVolt = [[0] * size_col for _ in range(size_row)]
    lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx = [0] * size(
        lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx
    )
    lib.s_AFC_Calc.VaAFC_U_RefCellVolt = [0] * size(lib.s_AFC_Calc.VaAFC_U_RefCellVolt)

    # Parameters/Calibrations, based on Volvo battery cell characterization
    # ------------------------------------------------
    lib.sAFC_P.Ve_U_CVFloatCellVolt = 4250
    lib.sAFC_P.Ve_U_SafetyMaxVolt = 4200
    lib.s_AFC_Param.KeAFC_U_CV_RatedChgCellVolt = 4250
    lib.s_AFC_Param.KeAFC_I_CV_ChgCurr = 30000
    lib.s_AFC_Param.KeAFC_I_CV_ChgStepCurr = 1000

    lib.s_AFC_Param.KaAFC_Pct_Stg_SOC = [
        1000,
        1530,
        2070,
        2600,
        3130,
        3650,
        4130,
        4570,
        4990,
        5380,
        5740,
        6070,
        6370,
        6650,
        6900,
        7130,
        7340,
        7530,
        7710,
        7860,
        8000,
        8490,
        8920,
        9300,
        9600,
    ]

    lib.s_AFC_Param.KaAFC_I_Stg_ChgMaxCurr = [  # mA
        345000,
        345000,
        345000,
        345000,
        345000,
        334000,
        311000,
        290000,
        270000,
        251000,
        232000,
        214000,
        197000,
        180000,
        165000,
        150000,
        136000,
        123000,
        111000,
        100000,
        90000,
        81000,
        72000,
        61000,
        50000,
    ]

    lib.s_AFC_Param.KaAFC_I_Stg_ChgMinCurr = [  # mA
        103000,
        103000,
        103000,
        103000,
        103000,
        92000,
        91000,
        80000,
        80000,
        80000,
        80000,
        74000,
        71000,
        66000,
        65000,
        65000,
        64000,
        55000,
        47000,
        46000,
        42000,
        36000,
        33000,
        31000,
        30000,
    ]

    lib.s_AFC_Param.KaAFC_I_Stg_ChgStepCurr = [  # mA
        11000,
        11000,
        11000,
        11000,
        11000,
        11000,
        10000,
        10000,
        10000,
        9000,
        8000,
        7000,
        6000,
        6000,
        5000,
        5000,
        4000,
        4000,
        4000,
        3000,
        3000,
        3000,
        3000,
        3000,
        2000,
    ]

    lib.s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt = [  # mV
        3870,
        3882,
        3906,
        3925,
        3944,
        3961,
        3969,
        3981,
        3999,
        4018,
        4031,
        4042,
        4052,
        4061,
        4068,
        4075,
        4083,
        4092,
        4101,
        4107,
        4113,
        4119,
        4125,
        4131,
        4137,
    ]

    lib.s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt = [5] * size(
        lib.s_AFC_Param.KaAFC_U_Stg_RefBandCellVolt
    )

    lib.s_AFC_Param.KaAFC_U_Stg_SADCellLim = [
        3958,
        3963,
        3993,
        4014,
        4039,
        4058,
        4069,
        4082,
        4100,
        4109,
        4121,
        4131,
        4140,
        4140,
        4144,
        4151,
        4158,
        4166,
        4174,
        4180,
        4184,
        4198,
        4206,
        4216,
        4228,
    ]

    lib.s_AFC_Param.KeAFC_T_CPV_MaxTempLim = 570
    lib.s_AFC_Param.KeAFC_T_CPV_MinTempLim = -100
    lib.s_AFC_Param.KeAFC_T_RefTemp = 350
    lib.s_AFC_Param.KeAFC_k_Coeff_a = 0.00012517
    lib.s_AFC_Param.KeAFC_k_Coeff_b = -0.01533200
    lib.s_AFC_Param.KeAFC_k_Coeff_c = 0.0000044631
    lib.s_AFC_Param.KeAFC_k_Coeff_d = 0.51427500
    lib.s_AFC_Param.KeAFC_k_Coeff_e = 0.00439800
    lib.s_AFC_Param.KeAFC_k_Coeff_f = 0.80011200
    lib.s_AFC_Param.KeAFC_k_Coeff_g = -0.00606000
    lib.s_AFC_Param.KeAFC_k_Coeff_h = 0.62772100

    lib.AFC_Param_VoltageImbalance.Ke_Cmp_SigmaLevel = 4
    lib.AFC_Param_VoltageImbalance.Ke_Cmp_NoiseFloor = 8
    lib.AFC_Param_VoltageImbalance.Ke_t_MinSamplingTime = 150
    lib.AFC_Param_VoltageImbalance.Ke_Cnt_ThresholdForValidSample = 10

    lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums = [0] * size(
        lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums)
    lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort = [0] * size(
        lib.AFC_VM_VoltageImbalance.Va_U_SE_ChargeVoltageSums_Sort)
    lib.AFC_VM_VoltageImbalance.Ve_Cnt_ExecutionCounter = 0
    lib.AFC_VM_VoltageImbalance.Ve_t_SamplingTime = 0
    lib.AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations = [0] * size(
        lib.AFC_VM_VoltageImbalance.Va_U_SE_AbsoluteVoltageSumDeviations)
    lib.AFC_VM_VoltageImbalance.Ve_b_ReadyForAnalysis = 0
    lib.AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags = [0] * size(
        lib.AFC_VM_VoltageImbalance.Va_b_VoltageImbalanceFlags)

    # Unused variables (commented for possibility of future implementations)
    # ------------------------------------------------
    # lib.g_num_temps = 4
    # lib.adc_VOLT_STACK = sum(lib.VaAPI_U_CellVolts)
    # lib.VeAPI_T_MaxTempSnsr = 4200
    # lib.adc_VOLT_MIN = 3000

    yield

    clean_dat_files(PROJECT_PATH)

def get_num_elements_from_buffer(lib):
    obj = ffi.addressof(lib.AFC_LoggingTrack[0], "Ne_Afc_Logging_Circ_Buff_Handle")
    data_ptr = ffi.new("uint16_t *")
    num_elements_inserted = ffi.cast("unsigned short *", data_ptr)
    #num_elements_inserted = ffi.new("uint16_t *")
    lib.LIB_CircBuffNumElementsInserted(obj, num_elements_inserted)
    return num_elements_inserted[0]

class LogParseResult:
    def __init__(self):
        self.indexes = []
        self.cycle_count = None
        self.stage = None
        self.highest_index = None
        self.temperatures = []

    def set_indexes(self, value):
        self.indexes = value

    def set_cycle_count(self, value):
        self.cycle_count = value

    def set_stage(self, value):
        self.stage = value

    def set_highest_index(self, value):
        self.highest_index = value

    def set_temperatures(self, value):
        self.temperatures = value

    def print_buffer(self):
        print(f"Log:  Indexes : {self.indexes}")
        print(f"Log:  Cycle Count : {self.cycle_count}")
        print(f"Log:  Stage : {self.stage}")
        print(f"Log:  Highest Index : {self.highest_index}")
        print(f"Log:  Temperatures : {self.temperatures}")
def process_log_buffer(lib, extn=1, write_to_file=False):
    """
    Process the log buffer and extract result, assign to return result data object of LogParseResult
    """
    result = LogParseResult()
    lfilename = f"log_buffer_{extn}.xlsx"
    log_data_fname = join(dirname(_MODULE_PATH), _TIME_BASED_OUTPUT_DATA, lfilename)
    log_data = {
        "Indexes": [],
        "Cycle_Count": [],
        "Stage": [],
        "Highest_index": [],
        "Temperatures": [],
    }

    # Get buffer (logged data) and parse
    obj = ffi.addressof(lib.AFC_LoggingTrack[0], "Ne_Afc_Logging_Circ_Buff_Handle")
    print(f"\nElements Inserted: {get_num_elements_from_buffer(lib)}")
    for i in range(extn):

        #ele_addr = ffi.new("uint8_t [18]")
        data_ptr = ffi.new("uint8_t [18]")
        ele_addr = ffi.cast("unsigned char *", data_ptr)
        # Get last logged element
        lib.LIB_CircBuffGetElement(obj, i, ele_addr)
        # Get and compare indexes logged
        result.indexes = [
            ele_addr[3],
            ele_addr[6],
            ele_addr[9],
            ele_addr[12],
            ele_addr[15],
        ]

        # Unpack buffer data
        py_list = ffi.unpack(ele_addr, _TOTAL_BYTES)
        print(py_list)
        #logger.debug(py_list)

        u32_word = int.from_bytes(bytes(py_list[:3]), byteorder="little", signed=False)
        result.cycle_count = 0xFFF & (u32_word >> 12)
        result.stage = 0x3F & (u32_word >> 6);
        result.highest_index = 0x3F & (u32_word >> 0);

        # Extract temperature logged
        result.temperatures = [
            int.from_bytes(py_list[4:6], byteorder="little", signed=True),
            int.from_bytes(py_list[7:9], byteorder="little", signed=True),
            int.from_bytes(py_list[10:12], byteorder="little", signed=True),
            int.from_bytes(py_list[13:15], byteorder="little", signed=True),
            int.from_bytes(py_list[16:18], byteorder="little", signed=True),
        ]
        print("\n\n RESULT \n\n")
        print(f"Warning Flags: {lib.VeAFC_e_ErrorFlags}")
        print(f"Early Flags: {lib.VeAFC_b_EarlyWarningAgingFlag}")
        print(f"Abnormal Flags: {lib.VeAFC_b_AbnormalAgingFlag}")
        print(f"Extreme Flags: {lib.VeAFC_b_ExtremeAgingFlag}")
        result.print_buffer()

        log_data["Indexes"].append(result.indexes)
        log_data["Cycle_Count"].append(result.cycle_count)
        log_data["Stage"].append(result.stage)
        log_data["Highest_index"].append(result.highest_index)
        log_data["Temperatures"].append(result.temperatures)
    if write_to_file:
        pass
        #(log_data, log_data_fname)
    return result

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    invoke_pytest(current_dir, html=MAKE_HTML)
