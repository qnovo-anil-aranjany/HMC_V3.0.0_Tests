"""Test Module Description:
    Test module for 'f_AFC_MainInit' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'f_AFC_MainInit'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

# === Uncomment the following line to skip all test cases in this module: ===
# pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 9601,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 25,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 30000,
                },
            },
            id="Test_Case_1_Initialize",
            marks=[
                mark.description(
                    "This test runs the 'f_AFC_MainInit' function and checks if initializations was properly executed."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_f_AFC_MainInit(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'f_AFC_MainInit' function.
    """

    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)

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
    # Run Function
    # ------------------------------------------------
    lib.f_AFC_MainInit()

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)
