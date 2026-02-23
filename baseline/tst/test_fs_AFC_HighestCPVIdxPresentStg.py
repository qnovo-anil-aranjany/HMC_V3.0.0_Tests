"""Test Module Description:
    Test module for 'fs_AFC_FindHighestCPVStageIdx' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_FindHighestCPVStageIdx'
    functions for the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
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
                "Inputs": {
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [i + 1 for i in range(10)]
                },
                "Expected": {
                    "highest_index": 10,
                },
            },
            id="Test_Case_1_HighestIndex",
            marks=[
                mark.description(
                    "This checks that the function return the highest index given 's_AFC_Calc.VaAFC_Cnt_CPVCorrIdx' "
                    "array."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_sf_HighestCPVIdxPresentStage(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_AFC_FindHighestCPVStageIdx' function.
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
    highest_index = lib.fs_AFC_FindHighestCPVStageIdx()

    # Compare Results
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["highest_index"], highest_index)


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [
            [19, 58, 42, 21, 45, 97, 81, 71, 80, 96],
            [32, 86, 20, 15, 78, 6, 62, 61, 57, 3],
            [100, 6, 54, 53, 16, 90, 36, 71, 16, 3],
            [82, 81, 44, 72, 3, 54, 86, 15, 47, 16],
            [93, 11, 80, 15, 91, 88, 7, 40, 48, 91],
            [32, 7, 28, 45, 31, 12, 100, 56, 55, 7],
            [19, 86, 98, 10, 45, 65, 84, 43, 77, 87],
            [73, 36, 25, 86, 84, 79, 74, 61, 61, 49],
            [64, 81, 18, 41, 10, 4, 79, 31, 46, 45],
            [40, 15, 19, 43, 63, 5, 30, 74, 67, 10],
        ],
        "KeINP_n_MaxNumCells": [0, 1, 5, 7, 10],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_sf_HighestCPVIdxPresentStage_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        set_lib_inputs(lib, test_cases)

        # Run Function
        # ------------------------------------------------
        highest_index = lib.fs_AFC_FindHighestCPVStageIdx()

        dict_record = {"highest_index": highest_index}

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            validate_test_cases(
                lib, test_cases, read_json_results, dict_to_compare=dict_record
            )

        # Log Stack-Parametrized Inputs
        # ------------------------------------------------
        if MAKE_HTML and LOG_STACK_PARAM_INPUTS:
            log_stack_parametrized_inputs(test_cases)

        # Optional: Log Stack-Parametrized Test Data
        # JSON file can be found in /buildoutputs/reports
        # ------------------------------------------------
        if WRITE_STACK_PARAM_RESULTS:
            record_test_data(
                lib, test_cases, write_json_results, dict_to_record=dict_record
            )
