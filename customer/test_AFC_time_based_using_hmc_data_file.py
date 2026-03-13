"""Test Module Description:
    Test module for CTE time based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *
import time
import os

SKIP_TEST = False

ACCEPTED_CHARGE_TIME_DEVIATION_PERCENTAGE = 15
if not SKIP_TEST:
    _INPUT_DIR = "test_data/time_based/input_data"
    _FILENAME = "1_HMC__260122_AFC+CTE_7784_MP1.1.8.0.0_Dsoc9to100_400kW_coolent30_45t.csv"
    LOG_FILE = _FILENAME.split(".")[0] + "_Log.txt"

    module_path = abspath(__file__)
    _OUTPUT_DIR = "test_data/time_based/output_data"
    output_path = join(dirname(module_path), _OUTPUT_DIR)
    log_file = join(output_path, f"Log_{LOG_FILE}")
    if os.path.exists(log_file):
        os.remove(log_file)

    _REFERENCE_DIR = "test_data/time_based/reference_data"
    reference_path = join(dirname(module_path), _REFERENCE_DIR)

    """
    Write logs to a file for later debugging.
    """
    def write_to_log(data):
        with open(log_file, 'a') as file:
            file.write(data)
            file.write("\n")

    """
    Parse data from csv file and populate Input structure
    """
    def parse_AFC_HMC_Data():
        input_path = join(dirname(module_path), _INPUT_DIR)
        csv_path = join(input_path, _FILENAME)

        test_cases = []

        # Open the CSV file
        # Iterate over each row in the CSV
        for row in iter_file(csv_path):
            # Get inputs
            test_filename = 'AFC_CTE_Behavioural_Test.csv'
            Time = int(ast.literal_eval(row["Time"]))
            PackSOC = int(row["Real soc"]) * 10
            PackSOC_DR = 1
            PackCurr = -int(row["Current"]) * 100
            PackCurr_DR = 1

            try:
                # CellVolts = [int(item) for item in ast.literal_eval(row["CellVolts"])]
                CellVolts = [int(row[f'cell_{i}']) for i in range(1, 193)]
            except TypeError:
                CellVolts = [int(row["CellVolts"])]

            try:
                # CellVolts_DR = [
                #     int(item) for item in ast.literal_eval(row["CellVolts_DR"])
                # ]
                CellVolts_DR = [1] * 192
            except TypeError:
                CellVolts_DR = [int(row["CellVolts_DR"])]

            try:
                # TempSnsrs = [int(item) for item in ast.literal_eval(row["TempSnsrs"])]
                TempSnsrs = [int(row[f'Temp_{i}_']) for i in range(0, 18)]
            except TypeError:
                TempSnsrs = [int(row["TempSnsrs"])]

            try:
                TempSnsrs_DR = [1] * 18
            except TypeError:
                TempSnsrs_DR = [int(row["TempSnsrs_DR"])]

            MinTempSnsr = int(min(TempSnsrs))
            MinTempSnsr_DR = 1

            MaxTempSnsr = int(max(TempSnsrs))
            MaxTempSnsr_DR = 1

            ChgPackCapcty = 125800
            ChgPackCapcty_DR = 1

            battery_state = row["cte_input_params.charging_now"]
            EVSEChgStatus = int(row["cte_input_params.charging_now"])
            # Format data for parametrized test
            test_case = {
                "Inputs": {
                    "filename": test_filename,
                    "Time": Time,
                    "PackSOC": PackSOC,
                    "PackSOC_DR": PackSOC_DR,
                    "PackCurr": PackCurr,
                    "PackCurr_DR": PackCurr_DR,
                    "CellVolts": CellVolts,
                    "CellVolts_DR": CellVolts_DR,
                    "TempSnsrs": TempSnsrs,
                    "TempSnsrs_DR": TempSnsrs_DR,
                    "MinTempSnsr": MinTempSnsr,
                    "MinTempSnsr_DR": MinTempSnsr_DR,
                    "MaxTempSnsr": MaxTempSnsr,
                    "MaxTempSnsr_DR": MaxTempSnsr_DR,
                    "ChgPackCapcty": ChgPackCapcty,
                    "ChgPackCapcty_DR": ChgPackCapcty_DR,
                    "battery_state": battery_state,
                    "EVSEChgStatus": EVSEChgStatus,
                },
                "Expected": {},
            }

            test_cases.append(test_case)
        return test_cases

    """
    Test case: time based test
    Read csv file, get parsed data in Input structure.
    Call AFC for each line from Input structure, populate AFC_CTE info structure.
    After each AFC call, call CTE for 10 times (each 100 ms)
    Receive CTE estimates and validate.
    """
    def test_hmc_afc_cte_behavioural(lib):
        all_time_steps = parse_AFC_HMC_Data()

        # Initialize results
        results = {
            "Filename": [],
            "Time": [],
            "StartSOC": [],
            "EndSOC": [],
            "Battery_State": [],
            "EVSEChgStatus": [],
            " ": [],
            "CTE_Status": [],
            "ErrorFlags (dec)": [],
            "ErrorFlags (bin)": [],
            "ChgPackCurr": [],
            "ChgPackVolt": [],
            "ChgCompletionFlag": [],
            "AFC_NVM_MagicNumber": [],
            "AFC_CTE_MagicNumber": [],
            "AFC_CTE_HighestIndex": [],
            "NVM_HighestIndex": [],
            "NVM_HighestIndex2": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (dec)": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (bin)": [],
            "QnovoAFC_LogVar2\nl_InitializedFlag": [],
            "QnovoAFC_LogVar3\nl_ValidSampleFlag": [],
            "QnovoAFC_LogVar4\nl_QNS_State": [],
            "QnovoAFC_LogVar5\nl_PresentStageNum": [],
            "QnovoAFC_LogVar6\nl_HighestIndex": [],
            "QnovoAFC_LogVar9\nl_CPVCorrIdx": [],
            "QnovoAFC_LogVar10\nl_CV_Curr": [],
            "QnovoAFC_LogVar11\nl_ProtocolStgCurr": [],
            "QnovoAFC_LogVar13\nl_ColdCompensatedCurr": [],
            "QnovoAFC_LogVar14\nl_CompensatedVolt": [],
            "QnovoAFC_LogVar15\nl_SampleCellVolt": [],
            "QnovoAFC_LogVar16\nl_RefCellVolt": [],
        }

        ele_addr = ffi.addressof(lib, "cte_status")
        status_ptr = ffi.cast("uint32_t*", ele_addr)
        lib.Qnovo_AFC_Init()
        test_i = 0
        for each_time_step in all_time_steps:
            test_i += 1
            # Initialize lib values before AFC call.
            test_filename = each_time_step["Inputs"]["filename"]
            input_time = each_time_step["Inputs"]["Time"]
            lib.VeAPI_I_PackCurr = each_time_step["Inputs"]["PackCurr"]
            lib.VeAPI_b_PackCurr_DR = each_time_step["Inputs"]["PackCurr_DR"]
            lib.VaAPI_U_CellVolts = each_time_step["Inputs"]["CellVolts"]
            lib.VaAPI_b_CellVolts_DR = each_time_step["Inputs"]["CellVolts_DR"]
            lib.VaAPI_T_TempSnsrs = each_time_step["Inputs"]["TempSnsrs"]
            lib.VaAPI_b_TempSnsrs_DR = each_time_step["Inputs"]["TempSnsrs_DR"]
            lib.VeAPI_T_MinTempSnsr = each_time_step["Inputs"]["MinTempSnsr"]
            lib.VeAPI_b_MinTempSnsr_DR = each_time_step["Inputs"]["MinTempSnsr_DR"]
            lib.VeAPI_T_MaxTempSnsr = each_time_step["Inputs"]["MaxTempSnsr"]
            lib.VeAPI_b_MaxTempSnsr_DR = each_time_step["Inputs"]["MaxTempSnsr_DR"]
            lib.VeAPI_Cap_ChgPackCapcty = each_time_step["Inputs"]["ChgPackCapcty"]
            lib.VeAPI_b_ChgPackCapcty_DR = each_time_step["Inputs"]["ChgPackCapcty_DR"]
            lib.VeAPI_Pct_PackSOC = each_time_step["Inputs"]["PackSOC"]
            lib.VeAPI_b_PackSOC_DR = each_time_step["Inputs"]["PackSOC_DR"]
            battery_state = each_time_step["Inputs"]["battery_state"]
            lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]

            # Call AFC
            while True:
                # Run Function
                # ------------------------------------------------
                lib.Qnovo_AFC(
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
                    lib.VeAPI_e_EVSEChgLevel,
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
                if lib.Output_SlicingStatus == 0:
                    break


            # Record results
            results["Filename"].append(test_filename)
            results["Time"].append(input_time)
            results["Battery_State"].append(battery_state)
            results["EVSEChgStatus"].append(lib.VeAPI_b_EVSEChgStatus)
            results[" "].append("")  # Divider between input and output
            results["ErrorFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
            results["ErrorFlags (bin)"].append(format(lib.VeAFC_e_ErrorFlags, "032b"))
            results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)
            results["CTE_Status"].append(lib.cte_status)
            results["ErrorFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
            results["ErrorFlags (bin)"].append(format(lib.VeAFC_e_ErrorFlags, "032b"))
            results["ChgPackCurr"].append(lib.VeAFC_I_ChgPackCurr)
            results["ChgPackVolt"].append(lib.VeAFC_U_ChgPackVolt)
            results["ChgCompletionFlag"].append(lib.VeAFC_b_ChgCompletionFlag)
            max_indices = [max(lib.s_AFC_Track.NtAFC_Cnt_CPVCorrIdx[i][j] for i in range(192)) for j in
                           range(15)]
            results["NVM_HighestIndex"].append(max_indices)

            results["NVM_HighestIndex2"].append(lib_array_to_list(lib.s_AFC_Track.NaAFC_Cnt_HighestCPVCorrIdx))

            results["QnovoAFC_LogVar1\nl_LoggingPath (dec)"].append(
                lib.QnovoAFC_LogVar1
            )
            results["QnovoAFC_LogVar1\nl_LoggingPath (bin)"].append(
                format(lib.QnovoAFC_LogVar1, "032b")
            )

            results["QnovoAFC_LogVar2\nl_InitializedFlag"].append(lib.QnovoAFC_LogVar2)

            results["QnovoAFC_LogVar3\nl_ValidSampleFlag"].append(
                lib_array_to_list(lib.QnovoAFC_LogVar3)
            )

            results["QnovoAFC_LogVar4\nl_QNS_State"].append(lib.QnovoAFC_LogVar4)
            results["QnovoAFC_LogVar5\nl_PresentStageNum"].append(lib.QnovoAFC_LogVar5)
            results["QnovoAFC_LogVar6\nl_HighestIndex"].append(lib.QnovoAFC_LogVar6)
            results["QnovoAFC_LogVar9\nl_CPVCorrIdx"].append(
                lib_array_to_list(lib.QnovoAFC_LogVar9)
            )
            results["QnovoAFC_LogVar10\nl_CV_Curr"].append(lib.QnovoAFC_LogVar10)
            results["QnovoAFC_LogVar11\nl_ProtocolStgCurr"].append(
                lib.QnovoAFC_LogVar11
            )
            results["QnovoAFC_LogVar13\nl_ColdCompensatedCurr"].append(lib.QnovoAFC_LogVar13)
            results["QnovoAFC_LogVar14\nl_CompensatedVolt"].append(
                lib_array_to_list(lib.QnovoAFC_LogVar14)
            )
            results["QnovoAFC_LogVar15\nl_SampleCellVolt"].append(
                lib_array_to_list(lib.QnovoAFC_LogVar15)
            )
            results["QnovoAFC_LogVar16\nl_RefCellVolt"].append(
                lib_array_to_list(lib.QnovoAFC_LogVar16)
            )

        # Write results into csv
        csv_path = join(output_path, f"processed_AFC_{_FILENAME}")
        write_output_to_excel(results, csv_path)
        if results["ChgPackCurr"]:
            output_pack_curr = results["ChgPackCurr"]
        # We have a reference file for output results.
        # Compare for regression.
        reference_file = join(reference_path, f"reference_AFC_{_FILENAME}")
        with open(reference_file, "r") as file:
            reader = csv.DictReader(file)
            reference_pack_cur = []
            for row in reader:
                reference_pack_cur.append(int(row["ChgPackCurr"]))
        compare_result(output_pack_curr, reference_pack_cur)

