"""Test Module Description:
    Test module AFC versioning.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


def test_Qnovo_AFC_Version(lib) -> None:
    """
    This test function performs verification of the AFC version.
    """

    # Compare Results
    # ------------------------------------------------
    compare_result(lib.get_afc_sw_ver(), 50602)
