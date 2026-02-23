"""Test Module Description:
    Test module for 'f_AFC_MainPrdc' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'f_AFC_MainPrdc'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = True  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")

_NVM_ARRAY_SIZE = 3750
_NUM_CELL = 192
_NUM_TEMP_SNSR = 18


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "VaAPI_Cmp_NVMRegion": [0] * _NVM_ARRAY_SIZE,
                    "VeAPI_I_PackCurr": 50000,
                    "VeAPI_b_PackCurr_DR": 1,
                    "VaAPI_U_CellVolts": [3200] * _NUM_CELL,
                    "VaAPI_b_CellVolts_DR": [1] * _NUM_CELL,
                    "VaAPI_T_TempSnsrs": [350] * _NUM_TEMP_SNSR,
                    "VaAPI_b_TempSnsrs_DR": [1] * _NUM_TEMP_SNSR,
                    "VeAPI_T_MinTempSnsr": 350,
                    "VeAPI_b_MinTempSnsr_DR": 1,
                    "VeAPI_T_MaxTempSnsr": 350,
                    "VeAPI_b_MaxTempSnsr_DR": 1,
                    "VeAPI_Cap_ChgPackCapcty": 16000,
                    "VeAPI_b_ChgPackCapcty_DR": 1,
                    "VeAPI_Pct_PackSOC": 5000,
                    "VeAPI_b_PackSOC_DR": 1,
                    "VeAPI_b_EVSEChgStatus": 1,
                    "VeAPI_e_EVSEChgLevel": 2,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 9,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 251000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_1_MainInit",
            marks=[
                mark.description("t=0s, Run MainInit"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 5000,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 9,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 251000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_2_MainPrdc",
            marks=[
                mark.description("t=1s, Run MainPrdc"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VaAPI_U_CellVolts": [4000] * _NUM_CELL,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 10,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [1] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 64,
                    "VeAFC_I_ChgPackCurr": 242000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_3_OverCPVLimit",
            marks=[
                mark.description(
                    "t=2s, enable tracking by being near 1% from end of stage"
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VaAPI_U_CellVolts": [4000] * _NUM_CELL,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 10,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 232000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_4_StartingNewStage",
            marks=[
                mark.description("t=3s, start a new stage"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 5740 - 50,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 10,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 232000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_5_TrackingEnabled",
            marks=[
                mark.description(
                    "t=4s, enable tracking by being near 1% from end of stage"
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 5741,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [1] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 232000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_6_EnterNewStageAttemptIncCPVIdx",
            marks=[
                mark.description("t=5s, attempt to increment CPV index"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 5741,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 214000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_7_ContinueInNewStage",
            marks=[
                mark.description("t=6s, continue with the new stage post attempt"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_b_EVSEChgStatus": 0,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 11,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_8_Reset Charging Status",
            marks=[
                mark.description("t=7s, set charging status to 0"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_b_EVSEChgStatus": 1,
                    "VeAPI_Pct_PackSOC": 5000,
                    "VaAPI_U_CellVolts": [3200] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 9,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [0] * _NUM_CELL,
                    "VeAFC_e_ErrorFlags": 0,
                    "VeAFC_I_ChgPackCurr": 251000,
                    "VeAFC_U_ChgPackVolt": 816000,
                },
            },
            id="Test_Case_9_RepeatEverything",
            marks=[
                mark.description("t=8s, Repeat as if test case 1 again"),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_Qnovo_AFC_1000ms_WorstCasePath(lib, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'f_AFC_MainPrdc' function.
    """

    # Setup Variables
    # ------------------------------------------------
    lib.s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt[9] = 3000
    lib.s_AFC_Param.KaAFC_U_Stg_RefStartCellVolt[10] = 3700
    lib.s_AFC_Param.KaAFC_U_Stg_SADCellLim[9] = 3340
    set_lib_inputs(lib, test_cases)

    if lib.VeAPI_b_EVSEChgStatus == 0:
        size_row, size_col = size(lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx)
        lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx = [[0] * size_col for _ in range(size_row)]

        size_row, size_col = size(lib.s_AFC_Track.NtAFC_U_RefCellVolt)
        lib.s_AFC_Track.NtAFC_U_RefCellVolt = [[0] * size_col for _ in range(size_row)]

    # Run Function
    # ------------------------------------------------
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
        ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
        ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag"),
        ffi.addressof(lib, "VeAFC_b_ExtremeAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_AbnormalAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_EarlyWarningAgingFlag"),
        ffi.addressof(lib, "VeAFC_b_EOLFlag"),
        ffi.addressof(lib, "VeAFC_b_SOCImbalanceFlag"),
    )

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)
