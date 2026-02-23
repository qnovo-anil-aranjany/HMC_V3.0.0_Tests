"""Test Module Description:
    Test module for 'fs_AFC_CalcTempCurrCompVolt' functions in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_CalcTempCurrCompVolt'
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
                    "VeAPI_Pct_PackSOC": 6371,
                    "VaAPI_U_CellVolts": [3200] * 10,
                    "VaAPI_T_TempSnsrs": [350] * 4,
                },
                "Expected": {"Le_U_CompensatedCellVolt": 3028},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "This checks for how voltage is compensated given a cell current and temperature."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "VeAPI_Pct_PackSOC": 1033,
                    "VaAPI_U_CellVolts": [3535] * 10,
                    "VaAPI_T_TempSnsrs": [266] * 4,
                },
                "Expected": {"Le_U_CompensatedCellVolt": 3600},
            },
            id="Test_Case_1",
            marks=[
                mark.description("Match On Chang calculations."),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_fs_AFC_CalcTempCurrCompVolt(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'fs_AFC_CalcTempCurrCompVolt'
    function.
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

    Le_U_CellOCV = lib.f_LIB_SOC_to_OCV(lib.VeAPI_Pct_PackSOC)
    Le_r_TemperatureRatio = lib.fs_AFC_CalcTemperatureRatio(lib.VaAPI_T_TempSnsrs[0])
    Le_r_CurrRatio = lib.fs_AFC_CalcCurrRatio()

    # Run Function
    # ------------------------------------------------
    Le_U_CompensatedCellVolt = lib.fs_AFC_CalcTempCurrCompVolt(
        lib.VaAPI_U_CellVolts[0], Le_U_CellOCV, Le_r_TemperatureRatio, Le_r_CurrRatio
    )

    # Compare Result
    # ------------------------------------------------
    compare_result(
        test_cases["Expected"]["Le_U_CompensatedCellVolt"],
        Le_U_CompensatedCellVolt,
    )


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "VeAPI_Pct_PackSOC": [x for x in range(0, 10000, 1000)],
        "VaAPI_U_CellVolts": [([x] * 10) for x in range(0, 4500, 500)],
        "VaAPI_T_TempSnsrs": [([x] * 4) for x in range(0, 600, 100)],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_CalcTempCurrCompVolt_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
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

        Le_U_CellOCV = lib.f_LIB_SOC_to_OCV(lib.VeAPI_Pct_PackSOC)
        Le_r_TemperatureRatio = lib.fs_AFC_CalcTemperatureRatio(
            lib.VaAPI_T_TempSnsrs[0]
        )
        Le_r_CurrRatio = lib.fs_AFC_CalcCurrRatio()

        # Run Function
        # ------------------------------------------------
        Le_U_CompensatedCellVolt = lib.fs_AFC_CalcTempCurrCompVolt(
            lib.VaAPI_U_CellVolts[0],
            Le_U_CellOCV,
            Le_r_TemperatureRatio,
            Le_r_CurrRatio,
        )

        dict_record = {"Le_U_CompensatedCellVolt": Le_U_CompensatedCellVolt}

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
