"""Test Module Description:
    Test module for 'fs_AFC_AttemptToIncCPVIdx' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'fs_AFC_AttemptToIncCPVIdx'
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
                "Inputs": {"Le_i_CPV_PresentIndex": 0},
                "Expected": {"Le_i_NewIndex": 1},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when stage = 10 and 'Le_i_CPV_PresentIndex' = 0."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 8},
                "Expected": {"Le_i_NewIndex": 9},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when stage = 10 and 'Le_i_CPV_PresentIndex' = 8."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 18},
                "Expected": {"Le_i_NewIndex": 19},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when stage = 10 and 'Le_i_CPV_PresentIndex' = 18."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 19},
                "Expected": {"Le_i_NewIndex": 19},
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when stage = 10 and 'Le_i_CPV_PresentIndex' = 19."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 100},
                "Expected": {"Le_i_NewIndex": 100},
            },
            id="Test_Case_5",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when stage = 10 and 'Le_i_CPV_PresentIndex' = 100."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 254},
                "Expected": {"Le_i_NewIndex": 254},
            },
            id="Test_Case_6",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when 'Le_i_CPV_PresentIndex' becomes unrealistically high."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
        param(
            {
                "Inputs": {"Le_i_CPV_PresentIndex": 255},
                "Expected": {"Le_i_NewIndex": 0},
            },
            id="Test_Case_7",
            marks=[
                mark.description(
                    "This checks for the 'Le_i_NewIndex' when 'Le_i_CPV_PresentIndex' reach max unsigned char value, "
                    "integer overflow in Le_i_NewIndex should reset to zero as it cannot represent 256."
                ),
                mark.jira_id("VCCFC-110"),
            ],
        ),
    ],
)
def test_fs_AFC_AttemptToIncCPVIdx(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the
    'fs_AFC_AttemptToIncCPVIdx' function.
    """

    # Setup Variables
    # ------------------------------------------------
    lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum = 10
    Le_i_CPV_PresentIndex = test_cases["Inputs"]["Le_i_CPV_PresentIndex"]
    # Run Function
    # ------------------------------------------------
    Le_i_NewIndex = lib.fs_AFC_AttemptToIncCPVIdx(Le_i_CPV_PresentIndex)

    # Compare Result
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["Le_i_NewIndex"], Le_i_NewIndex)


# =======================================================================
# Stack-Parametrize Test Cases for Code Coverage
# =======================================================================
if RUN_STACK_PARAM_TESTS:
    param_inputs = {
        "Le_i_PresentStageIdx": [x for x in range(0, 41, 2)],
        "s_AFC_Calc.VeAFC_Cnt_PresentStgNum": [x for x in range(0, 25, 2)],
    }

    combinations, ids = parametrize_args(param_inputs)

    @pytest.mark.parametrize("test_cases", combinations, ids=ids)
    @pytest.mark.jira_id("VCCFC-110")
    def test_fs_AFC_AttemptToIncCPVIdx_coverage(
        lib, setup_parameters, test_cases, read_json_results, write_json_results
    ) -> None:
        """
        This test function executes stack parametrization tests across a range of input conditions to achieve improved
        code coverage.
        """

        # Setup Variables
        # ------------------------------------------------
        Le_i_PresentStageIdx = test_cases["Inputs"]["Le_i_PresentStageIdx"]

        set_lib_inputs(lib, test_cases)

        # Run Function
        # ------------------------------------------------
        Le_i_NewIndex = lib.fs_AFC_AttemptToIncCPVIdx(Le_i_PresentStageIdx)

        dict_record = {"Le_i_NewIndex": Le_i_NewIndex}

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
