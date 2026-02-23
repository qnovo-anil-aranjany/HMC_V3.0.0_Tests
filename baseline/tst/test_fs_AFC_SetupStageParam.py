"""Test Module Description:
    Test module for 'fs_AFC_SetupStageParam' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_SetupStageParam'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - VCCFC-110
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

RUN_STACK_PARAM_TESTS = True  # Set True to run stack-parametrized testing.
LOG_STACK_PARAM_INPUTS = True  # Set True to log stack-parametrized inputs into html.
WRITE_STACK_PARAM_RESULTS = (
    False  # Set True to write stack-parametrized results into JSON.
)

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {"VeAPI_Pct_PackSOC": 9601},
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 25,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 30000,
                },
            },
            id="Test_Case_1_ConstantVoltage",
            marks=[
                mark.description(
                    "This checks that the stage is not incremented under high SOC conditions (i.e. constant voltage "
                    "scenario)."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"VeAPI_Pct_PackSOC": 6370},
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 13,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [0] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [0] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 180000,
                },
            },
            id="Test_Case_2_IncrementStages",
            marks=[
                mark.description(
                    "This checks that under normal operating conditions, 's_AFC_Calc.VeAFC_Cnt_PresentStgNum' is "
                    "incremented to the correct stage based on SOC."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"VeAPI_Pct_PackSOC": 8490},
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 22,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 72000,
                },
            },
            id="Test_Case_3_NotCPVStage",
            marks=[
                mark.description(
                    "This checks for when not in CPV condition, the function should not reset both "
                    "'s_AFC_Calc.VaAFC_b_ValidSampleFlag' and 's_AFC_Calc.VaAFC_U_SampleCellVolt'."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 0,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 26,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 26,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 30000,
                },
            },
            id="Test_Case_4_ExceedMaxStage",
            marks=[
                mark.description(
                    "This checks whether the function will further increment 's_AFC_Calc.VeAFC_Cnt_PresentStgNum' in the edge case where it "
                    "has already surpassed the maximum stage."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"VeAPI_Pct_PackSOC": 0},
                "Expected": {
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 0,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [0] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [0] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 345000,
                },
            },
            id="Test_Case_5_ZeroStage",
            marks=[
                mark.description(
                    "This checks whether the function increments 's_AFC_Calc.VeAFC_Cnt_PresentStgNum' in the specific edge case where "
                    "both 's_AFC_Calc.VeAFC_Cnt_PresentStgNum' and 'VeAPI_Pct_PackSOC' are zero."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_fs_AFC_SetupStageParam(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'fs_AFC_SetupStageParam'
    function.
    """

    # Setup Variables
    # ------------------------------------------------
    lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag = [1] * size(
        lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag
    )
    lib.s_AFC_Calc.VaAFC_U_SampleCellVolt = [3200] * size(
        lib.s_AFC_Calc.VaAFC_U_SampleCellVolt
    )
    lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx = [5] * size(
        lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx
    )

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
    lib.fs_AFC_SetupStageParam()

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "VeAPI_Pct_PackSOC": [x for x in range(0, 10001, 2000)],
        "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": [x for x in range(0, 27, 2)],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_SetupStageParam_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag = [1] * size(
            lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag
        )
        lib.s_AFC_Calc.VaAFC_U_SampleCellVolt = [3200] * size(
            lib.s_AFC_Calc.VaAFC_U_SampleCellVolt
        )
        lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx = [5] * size(
            lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx
        )

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
        lib.fs_AFC_SetupStageParam()

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            validate_test_cases(lib, test_cases, read_json_results)

        # Log Stack-Parametrized Inputs
        # ------------------------------------------------
        if MAKE_HTML and LOG_STACK_PARAM_INPUTS:
            log_stack_parametrized_inputs(test_cases)

        # Optional: Log Stack-Parametrized Test Data
        # JSON file can be found in /buildoutputs/reports
        # ------------------------------------------------
        if WRITE_STACK_PARAM_RESULTS:
            vars_record = [
                "s_AFC_Calc.VeAFC_Cnt_PresentStgNum",
                "s_AFC_Calc.VaAFC_b_ValidSampleFlag",
                "s_AFC_Calc.VaAFC_U_SampleCellVolt",
                "VeAFC_U_ChgPackVolt",
                "VeAFC_I_ChgPackCurr",
            ]

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record
            )
