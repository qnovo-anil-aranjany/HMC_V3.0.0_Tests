"""Test Module Description:
    Test module for 'LIB_LogData' function in the shared common libraries.

    This test group contains pytest test cases designed to ensure that the 'LIB_LogData'
    functions in the fast charging algorithm works as expected under various scenarios.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.12.4
    - Pytest version >= 8.0.1
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

ffi = cffi.FFI()


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {"VeAPI_Cmp_LogSrc": 10484130, "Obsfuscated_Result": 2068088894},
                "Expected": {"Result": 10484130},
                "Desc": "This checks VeAPI_Cmp_LogSrc is correct.",
            },
            id="Test_Case_1",
        ),
        param(
            {
                "Inputs": {"VeAPI_Cmp_LogSrcArray":  [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                            "Obsfuscated_Result": [2071690103, 2071690101, 2071690091, 2071690089, 2071690095, 2071690093,
                                                    2071690083, 2071690081, 2071690087, 2071690085, 2071690075, 2071690073,
                                                    2071690079, 2071690077, 2071690067]},
                "Expected": {"Result": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]},
                "Desc": "This checks VeAPI_Cmp_LogSrcArray is correct.",
            },
            id="Test_Case_1",
        ),
    ],
)

# NOTE: The results from the higher temp and lower temp are the same
def test_afc_obfuscation(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of Diagnostic interface functions and compliance with API
    """

    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    if "VeAPI_Cmp_LogSrc" in test_cases["Inputs"]:
        lib.LIB_Obfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrc"), 4, 0xBD
        )
        lib.VeAPI_Cmp_LogSrc = test_cases["Inputs"]["Obsfuscated_Result"]
        lib.LIB_Deobfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrc"), 4, 0xBD
        )
        expected = test_cases["Expected"]["Result"]
        actual = lib.VeAPI_Cmp_LogSrc
        compare_result(expected, actual)

    if "VeAPI_Cmp_LogSrcArray" in test_cases["Inputs"]:
        lib.LIB_Obfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrcArray"), lib.VeAPI_Cmp_LogSrcArraySize, 0xBD
        )

        lib.VeAPI_Cmp_LogSrcArray = test_cases["Inputs"]["Obsfuscated_Result"]
        lib.LIB_Deobfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrcArray"), lib.VeAPI_Cmp_LogSrcArraySize, 0xBD
        )
        expected = test_cases["Expected"]["Result"]
        actual = list(lib.VeAPI_Cmp_LogSrcArray)
        compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {"VeAPI_Cmp_LogSrc": 10484130, "Obsfuscated_Result": 2068088894},
                "Expected": {"Result": 10484130},
                "Desc": "This checks VeAPI_Cmp_LogSrc is correct.",
            },
            id="Test_Case_1",
        ),
        param(
            {
                "Inputs": {"VeAPI_Cmp_LogSrcArray":  [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                            "Obsfuscated_Result": [2071690103, 2071690101, 2071690091, 2071690089, 2071690095, 2071690093,
                                                    2071690083, 2071690081, 2071690087, 2071690085, 2071690075, 2071690073,
                                                    2071690079, 2071690077, 2071690067]},
                "Expected": {"Result": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]},
                "Desc": "This checks VeAPI_Cmp_LogSrcArray is correct.",
            },
            id="Test_Case_1",
        ),
    ],
)

# NOTE: The results from the higher temp and lower temp are the same
def test_afc_cte_obfuscation(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of Diagnostic interface functions and compliance with API
    """

    # Setup Variables
    # ------------------------------------------------
    set_lib_inputs(lib, test_cases)

    # Run Function
    # ------------------------------------------------
    if "VeAPI_Cmp_LogSrc" in test_cases["Inputs"]:
        lib.LIB_Obfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrc"), 4, 0xBD
        )
        lib.VeAPI_Cmp_LogSrc = test_cases["Inputs"]["Obsfuscated_Result"]
        lib.LIB_DeobfuscateCTE(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrc"), 4, 0xBD
        )
        expected = test_cases["Expected"]["Result"]
        actual = lib.VeAPI_Cmp_LogSrc
        compare_result(expected, actual)

    if "VeAPI_Cmp_LogSrcArray" in test_cases["Inputs"]:
        lib.LIB_Obfuscate(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrcArray"), lib.VeAPI_Cmp_LogSrcArraySize, 0xBD
        )

        lib.VeAPI_Cmp_LogSrcArray = test_cases["Inputs"]["Obsfuscated_Result"]
        lib.LIB_DeobfuscateCTE(
            ffi.addressof(lib, "VeAPI_Cmp_LogSrcArray"), lib.VeAPI_Cmp_LogSrcArraySize, 0xBD
        )
        expected = test_cases["Expected"]["Result"]
        actual = list(lib.VeAPI_Cmp_LogSrcArray)
        compare_result(expected, actual)