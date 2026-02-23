"""Test Module Description:
    Test module for 'fs_AFC_CalcTempCompChgCurr' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_CalcTempCompChgCurr'
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
                "Inputs": {"Le_T_CellTemp": -10},
                "Expected": {"Le_U_CompensatedCurr": 5176},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is -1.0 celsius."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_T_CellTemp": 0},
                "Expected": {"Le_U_CompensatedCurr": 5239},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is 0 celsius."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_T_CellTemp": 150},
                "Expected": {"Le_U_CompensatedCurr": 6848},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is 15.0 celsius."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_T_CellTemp": 340},
                "Expected": {"Le_U_CompensatedCurr": 9845},
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is 34.0 celsius."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_T_CellTemp": 350},
                "Expected": {"Le_U_CompensatedCurr": 10000},
            },
            id="Test_Case_5",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is 35.0 celsius."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_T_CellTemp": 32767},
                "Expected": {"Le_U_CompensatedCurr": 10000},
            },
            id="Test_Case_6",
            marks=[
                mark.description(
                    "This checks current compensation when Cell temperature is at unrealistically high value."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
# NOTE: The results from the higher temp and lower temp are the same
def test_fs_AFC_CalcTempCompChgCurr(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'fs_AFC_CalcTempCompChgCurr'
    function.
    """

    # Setup Variables
    # ------------------------------------------------
    chg_current = 10000
    Le_T_CellTemp = test_cases["Inputs"]["Le_T_CellTemp"]

    # Run Function
    # ------------------------------------------------
    Le_U_CompensatedCurr = lib.fs_AFC_CalcTempCompChgCurr(chg_current, Le_T_CellTemp)

    # Compare Results
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["Le_U_CompensatedCurr"], Le_U_CompensatedCurr)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "s_AFC_Param.KeAFC_k_Coeff_a": 0.00011866,  # New: 0.00011866, Old: 0.00012517
                    "s_AFC_Param.KeAFC_k_Coeff_b": -0.02089035,  # New: -0.02089035, Old: -0.01533200
                    "s_AFC_Param.KeAFC_T_RefTemp": 250,
                    "s_AFC_Calc.VeAFC_T_StdU_RefCellTemp": 250.0 / 10.0,
                    "Le_T_CellTemp": 247,
                    "Le_I_ChgCurr": 214000,
                },
                "Expected": {"Le_U_CompensatedCurr": 212656},
            },
            id="Test_Case_7_Match",
            marks=[
                mark.description(
                    "This test checks if this function matches On Chang's expected results."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
# NOTE: The results from the higher temp and lower temp are the same
def test_fs_AFC_CalcTempCompChgCurr_behavioral(
    lib, setup_parameters, test_cases
) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_AFC_CalcTempCompChgCurr' function.
    """

    # Setup Variables
    # ------------------------------------------------
    Le_I_ChgCurr = test_cases["Inputs"]["Le_I_ChgCurr"]
    Le_T_CellTemp = test_cases["Inputs"]["Le_T_CellTemp"]
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    Le_U_CompensatedCurr = lib.fs_AFC_CalcTempCompChgCurr(Le_I_ChgCurr, Le_T_CellTemp)

    # Compare Results
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["Le_U_CompensatedCurr"], Le_U_CompensatedCurr)


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "chg_current": [x for x in range(0, 10000, 500)],
        "Cell_temp": [x for x in range(0, 600, 50)],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_CalcTempCompChgCurr_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        chg_current = test_cases["Inputs"]["chg_current"]
        Cell_temp = test_cases["Inputs"]["Cell_temp"]

        # Run Function
        # ------------------------------------------------
        Le_U_CompensatedCurr = lib.fs_AFC_CalcTempCompChgCurr(chg_current, Cell_temp)

        dict_record = {"Le_U_CompensatedCurr": Le_U_CompensatedCurr}

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
