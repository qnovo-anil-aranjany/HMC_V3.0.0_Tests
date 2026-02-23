"""Test Module Description:
    Test module for 'fs_AFC_CPVTrack' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_CPVTrack'
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
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3900] * 10,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [5] * 10,
                    "s_AFC_Calc.VaAFC_U_RefCellVolt": [3100] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [6] * 10,
                    "s_AFC_Calc.VaAFC_U_RefCellVolt": [3105] * 10,
                },
            },
            id="Test_Case_1_Tracking",
            marks=[
                mark.description(
                    "This checks the condition when CPV tracking is active, 's_AFC_Calc.VaAFC_Cnt_CPVCorrIdx' is "
                    "incremented by one and 's_AFC_Calc.VaAFC_U_RefCellVolt' was correctly calculated."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_fs_AFC_CPVTrack(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'fs_AFC_CPVTrack'
    function.
    """

    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)
    lib.KeINP_n_NumCellsPerSliceForCompensation= 10
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
    lib.fs_AFC_CPVTrack1()
    lib.fs_AFC_CPVTrack2()

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": [0, 5, 10],
        "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [
            [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        ],
        "s_AFC_Calc.VaAFC_U_SampleCellVolt": [
            [2750, 250, 1000, 2000, 1250, 3750, 2500, 3500, 500, 750],
            [3500, 3000, 3250, 1500, 4500, 4000, 0, 4250, 3750, 2750],
            [4500, 2500, 3250, 250, 4000, 3000, 500, 2750, 1250, 4250],
            [0, 2750, 1500, 250, 3250, 2250, 1750, 1250, 500, 1000],
        ],
        "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [
            [19, 58, 42, 21, 45, 97, 81, 71, 80, 96],
            [32, 86, 20, 15, 78, 6, 62, 61, 57, 3],
            [100, 6, 54, 53, 16, 90, 36, 71, 16, 3],
            [40, 15, 19, 43, 63, 5, 30, 74, 67, 10],
        ],
        "s_AFC_Calc.VaAFC_U_RefCellVolt": [
            [2750, 250, 1000, 2000, 1250, 3750, 2500, 3500, 500, 750],
            [3500, 3000, 3250, 1500, 4500, 4000, 0, 4250, 3750, 2750],
            [4500, 2500, 3250, 250, 4000, 3000, 500, 2750, 1250, 4250],
            [500, 2000, 750, 1000, 3500, 2500, 2250, 1750, 1250, 2750],
            [0, 2750, 1500, 250, 3250, 2250, 1750, 1250, 500, 1000],
        ],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_CPVTrack_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        set_lib_inputs(lib, test_cases)
        lib.KeINP_n_NumCellsPerSliceForCompensation = lib.KeINP_n_MaxNumCells
        # Run Function
        # ------------------------------------------------
        lib.fs_AFC_CPVTrack1()
        lib.fs_AFC_CPVTrack2()

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
                "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx",
                "s_AFC_Calc.VaAFC_U_RefCellVolt",
            ]

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record
            )
