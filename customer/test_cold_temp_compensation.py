

"""Test Module Description:
    Test module for 'AFC_ColdTempCompensation' function in the fast charging algorithm.

    This test group contains pytest test cases designed to ensure that the 'AFC_ColdTempCompensation'
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
MAKE_HTML = True
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
def test_AFC_ColdTempCompensation(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of specific operating conditions relevant to the 'AFC_ColdTempCompensation'
    function.
    """

    # Setup Variables
    # ------------------------------------------------
    chg_current = 10000
    Le_T_CellTemp = test_cases["Inputs"]["Le_T_CellTemp"]

    # Run Function
    # ------------------------------------------------
    Le_U_CompensatedCurr = lib.fs_AFC_CalcTempCompChgCurr(chg_current, Le_T_CellTemp)

    # Use these lines for updating testrail when required
    # log_for_testrail_update("AFC_ColdTempCompensation")
    print(f"ACTUAL: {Le_U_CompensatedCurr}")

    # Compare Results
    # ------------------------------------------------
    compare_result(test_cases["Expected"]["Le_U_CompensatedCurr"], Le_U_CompensatedCurr)