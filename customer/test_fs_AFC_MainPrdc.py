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
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

RUN_STACK_PARAM_TESTS = False  # Set True to run stack-parametrized testing.
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
                    "tracking_flag": 0,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 1,
                    "VeAPI_Pct_PackSOC": 9601,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 192,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 192,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [5] * 192,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 19,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 25200,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 192,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3200] * 192,
                    "VeAFC_U_ChgPackVolt": 806400,
                    "VeAFC_I_ChgPackCurr": 30200,
                },
            },
            id="Test_Case_1_Start_New_Stage",
            marks=[
                mark.description(
                    "This test checks the various conditions when 's_AFC_Calc.VeAFC_e_QNS_State' is in START_STAGE and "
                    "ensure that the value of 's_AFC_Calc.VeAFC_e_QNS_State' changes from START_STAGE to "
                    "CeAFC_e_ContinueStage after execution."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "tracking_flag": 1,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "VeAPI_Pct_PackSOC": 6371,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 192,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3900] * 192,
                    "s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx": [5] * 192,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 1,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 13,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 30000,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 192,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3900] * 192,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 167000,
                },
            },
            id="Test_Case_2_CeAFC_e_ContinueStage",
            marks=[
                mark.description(
                    "This checks the main periodic under normal operating conditions in CONTINUE STAGE, specifically "
                    "during a stage transition due to SOC, executes CPV tracking and increment the stage."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "tracking_flag": 1,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "VeAPI_Pct_PackSOC": 6371,
                    "VaAPI_U_CellVolts": [4500] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 1,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 13,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 30000,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [0] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [0] * 10,
                    "VeAFC_U_ChgPackVolt": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="Test_Case_3_Over_Safety",
            marks=[
                mark.description(
                    "This checks for the scenario when cell voltages exceed the cell safety limit which triggers the "
                    "'Le_b_OverFlag' and forces increment to the next stage."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "tracking_flag": 1,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "VeAPI_Pct_PackSOC": 6371,
                    "s_AFC_Param.KaAFC_U_Stg_SADCellLim": [0] * 25,
                    "VaAPI_U_CellVolts": [4200] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 1,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 13,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 30000,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [0] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [0] * 10,
                    "VeAFC_U_ChgPackVolt": 0,
                    "VeAFC_I_ChgPackCurr": 0,
                },
            },
            id="Test_Case_4_Over_CPV",
            marks=[
                mark.description(
                    "This checks for the scenario when cell voltages exceed the cell SAD limit which triggers the "
                    "'Le_b_OverCPVFlag' and forces increment to the next stage."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "tracking_flag": 1,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "VeAPI_Pct_PackSOC": 6370 - 100,
                    "VaAPI_U_CellVolts": [3200] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 12,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 30000,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [1] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [3442] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 197000,
                },
            },
            id="Test_Case_5_GetSampleVoltage",
            marks=[
                mark.description(
                    "This checks for the condition when SOC is near the end of the stage (1%) to trigger the "
                    "conditions to get sample voltages for CPV tracking, therefore 's_AFC_Calc.VaAFC_b_ValidSampleFlag' == True."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "tracking_flag": 1,
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 25,
                    "VeAPI_Pct_PackSOC": 9800,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 30000,  # assume controller initialized in constant voltage.
                    "VaAPI_U_CellVolts": [4250] * 10,
                },
                "Expected": {
                    "s_AFC_Calc.VeAFC_e_QNS_State": 2,
                    "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": 25,
                    "s_AFC_Calc.VeAFC_I_CV_Curr": 29000,
                    "s_AFC_Calc.VaAFC_b_ValidSampleFlag": [0] * 10,
                    "s_AFC_Calc.VaAFC_U_SampleCellVolt": [0] * 10,
                    "VeAFC_U_ChgPackVolt": 42500,
                    "VeAFC_I_ChgPackCurr": 29000,
                },
            },
            id="Test_Case_6_ConstantVoltage",
            marks=[
                mark.description(
                    "This checks the scenario when in constant voltage condition, 's_AFC_Calc.VeAFC_Cnt_PresentStgNum' should not "
                    "increment further, output current should be based off 's_AFC_Calc.VeAFC_I_CV_Curr' and output voltage should "
                    "be based off of 's_AFC_Param.KeAFC_U_CV_FloatCellVolt'."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_f_AFC_MainPrdc(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'f_AFC_MainPrdc' function.
    """

    # Setup Variables
    # ------------------------------------------------
    tracking_flag = test_cases["Inputs"]["tracking_flag"]
    set_lib_inputs(lib, test_cases)
    lib.KeINP_n_NumCellsPerSliceForCompensation = 10
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
        ffi.addressof(lib, "Output_SlicingStatus"),
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
    lib.Afc_Slices = 0
    print(f"VeAFC_U_ChgPackVolt: {lib.VeAFC_U_ChgPackVolt}")
    #print(f"VeAfcState: {lib.VeAfcState}")
    # Run Function
    # ------------------------------------------------
    for i in range(10):
        lib.f_AFC_MainPrdc(tracking_flag)

    # Compare Results
    # ------------------------------------------------
    validate_test_cases(lib, test_cases)


# =======================================================================
# Stack-Parametrized Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "VeAPI_Pct_PackSOC": [50, 7900, 10000],
        "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": [0, 20, 22, 25],
        "s_AFC_Calc.VeAFC_e_QNS_State": [0, 1, 2],
        "VaAPI_U_CellVolts": [([x] * 10) for x in [0, 3500, 4200, 4500]],
        "VeAPI_T_MinTempSnsr": [0, 360],
        "VeAPI_T_MaxTempSnsr": [550, 990],
        "KeINP_n_MaxNumCells": [1, 10],
        "Le_b_CPVTrackingFlag": [0, 1],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_f_AFC_MainPrdc_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        tracking_flag = test_cases["Inputs"]["Le_b_CPVTrackingFlag"]
        set_lib_inputs(lib, test_cases)
        lib.KeINP_n_NumCellsPerSliceForCompensation = lib.KeINP_n_MaxNumCells
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
            ffi.addressof(lib, "Output_SlicingStatus"),
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
        lib.Afc_Slices = 0
        # Run Function
        # ------------------------------------------------
        #lib.f_AFC_MainPrdc(tracking_flag)

        for i in range(10):
            lib.f_AFC_MainPrdc(tracking_flag)

        # Compare Results
        # ------------------------------------------------
        if not WRITE_STACK_PARAM_RESULTS:
            if lib.s_AFC_Calc.VeAFC_I_CV_Curr >= 1590138752:
                pytest.xfail(
                    "Known issue where signed to unsigned changes 's_AFC_Calc.VeAFC_I_CV_Curr' results from -1000A."
                )
            else:
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
                "s_AFC_Calc.VeAFC_e_QNS_State",
                "s_AFC_Calc.VeAFC_Cnt_PresentStgNum",
                "s_AFC_Calc.VeAFC_I_CV_Curr",
                "s_AFC_Calc.VaAFC_b_ValidSampleFlag",
                "s_AFC_Calc.VaAFC_U_SampleCellVolt",
                "VeAFC_U_ChgPackVolt",
                "VeAFC_I_ChgPackCurr",
            ]

            record_test_data(
                lib, test_cases, write_json_results, var_to_record=vars_record
            )
