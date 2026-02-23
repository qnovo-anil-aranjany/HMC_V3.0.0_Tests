"""Test Module Description:
    Test module for HSD time-based testing.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .__main__ import *

SKIP_TEST = True

if not SKIP_TEST:
    _SUBDIR_NAME = "time_based_data"
    _FILENAME = "processed_Behavioral_Test_20240423"

    CeAFC_cmp_LogOffsetZero = 0
    CeAFC_cmp_LogOffset = 43
    CeAFC_I_LogOffset = 502673
    CeAPI_b_LogOffsetZero = 0

    def parse_AFC_processed_Behavioral_Test_20240423():
        module_path = abspath(__file__)
        dir_path = join(dirname(module_path), _SUBDIR_NAME)
        csv_path = join(dir_path, f"{_FILENAME}.csv")

        test_cases = []

        # Open the CSV file
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)

            # Iterate over each row in the CSV
            for row in reader:
                # Get inputs
                test_filename = row["Filename"]
                Time = int(row["Time"])
                PackSOC = int(row["PackSOC"])
                PackSOC_DR = int(row["PackSOC_DR"])
                PackCurr = int(row["PackCurr"])
                PackCurr_DR = int(row["PackCurr_DR"])

                CellVolts = [int(item) for item in ast.literal_eval(row["CellVolts"])]

                CellVolts_DR = [
                    int(item) for item in ast.literal_eval(row["CellVolts_DR"])
                ]

                TempSnsrs = [int(item) for item in ast.literal_eval(row["TempSnsrs"])]

                TempSnsrs_DR = [
                    int(item) for item in ast.literal_eval(row["TempSnsrs_DR"])
                ]

                MinTempSnsr = int(row["MinTempSnsr"])
                MinTempSnsr_DR = int(row["MinTempSnsr_DR"])

                MaxTempSnsr = int(row["MaxTempSnsr"])
                MaxTempSnsr_DR = int(row["MaxTempSnsr_DR"])

                ChgPackCapcty = int(row["ChgPackCapcty"])
                ChgPackCapcty_DR = int(row["ChgPackCapcty_DR"])

                Battery_State = row["Battery_State"]
                EVSEChgStatus = int(row["EVSEChgStatus"])

                logged_VeAFC_b_Initialized = max(
                    0,
                    int(row["QnovoAFC_LogVar2\nl_InitializedFlag"])
                    - CeAPI_b_LogOffsetZero,
                )
                logged_VeAFC_e_QNS_State = max(
                    0, int(row["QnovoAFC_LogVar4\nl_QNS_State"]) - CeAFC_cmp_LogOffset
                )
                logged_VeAFC_Cnt_PresentStgNum = max(
                    0,
                    int(row["QnovoAFC_LogVar5\nl_PresentStageNum"])
                    - CeAFC_cmp_LogOffset,
                )
                logged_VeAFC_I_CV_Curr = max(
                    0, int(row["QnovoAFC_LogVar10\nl_CV_Curr"]) - CeAFC_I_LogOffset
                )

                logged_VaAFC_b_ValidSampleFlag = [
                    max(0, (int(item) - CeAFC_cmp_LogOffsetZero))
                    for item in ast.literal_eval(
                        row["QnovoAFC_LogVar3\nl_ValidSampleFlag"]
                    )
                ]

                logged_VaAFC_U_SampleCellVolt = [
                    max(0, (int(item) - CeAFC_cmp_LogOffsetZero))
                    for item in ast.literal_eval(
                        row["QnovoAFC_LogVar15\nl_SampleCellVolt"]
                    )
                ]

                logged_VaAFC_Cnt_CPVCorrIdx = [
                    max(0, (int(item) - CeAFC_cmp_LogOffsetZero))
                    for item in ast.literal_eval(row["QnovoAFC_LogVar9\nl_CPVCorrIdx"])
                ]
                logged_VaAFC_U_RefCellVolt = [
                    max(0, (int(item) - CeAFC_cmp_LogOffsetZero))
                    for item in ast.literal_eval(
                        row["QnovoAFC_LogVar16\nl_RefCellVolt"]
                    )
                ]

                # Format data for parametrized test
                test_case = {
                    "Inputs": {
                        "Filename": test_filename,
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
                        "Battery_State": Battery_State,
                        "EVSEChgStatus": EVSEChgStatus,
                        "logged_VeAFC_b_Initialized": logged_VeAFC_b_Initialized,
                        "logged_VeAFC_e_QNS_State": logged_VeAFC_e_QNS_State,
                        "logged_VeAFC_Cnt_PresentStgNum": logged_VeAFC_Cnt_PresentStgNum,
                        "logged_VeAFC_I_CV_Curr": logged_VeAFC_I_CV_Curr,
                        "logged_VaAFC_b_ValidSampleFlag": logged_VaAFC_b_ValidSampleFlag,
                        "logged_VaAFC_U_SampleCellVolt": logged_VaAFC_U_SampleCellVolt,
                        "logged_VaAFC_Cnt_CPVCorrIdx": logged_VaAFC_Cnt_CPVCorrIdx,
                        "logged_VaAFC_U_RefCellVolt": logged_VaAFC_U_RefCellVolt,
                    },
                    "Expected": {},
                }

                test_cases.append(test_case)

        return test_cases

    def test_AFC_processed_Behavioral_Test_20240423(lib):
        all_time_steps = parse_AFC_processed_Behavioral_Test_20240423()

        start_time = 3102

        # Initialize results
        results = {
            "Filename": [],
            "Time": [],
            "PackCurr": [],
            "PackCurr_DR": [],
            "CellVolts": [],
            "CellVolts_DR": [],
            "TempSnsrs": [],
            "TempSnsrs_DR": [],
            "MinTempSnsr": [],
            "MinTempSnsr_DR": [],
            "MaxTempSnsr": [],
            "MaxTempSnsr_DR": [],
            "ChgPackCapcty": [],
            "ChgPackCapcty_DR": [],
            "PackSOC": [],
            "PackSOC_DR": [],
            "Battery_State": [],
            "EVSEChgStatus": [],
            " ": [],
            "ErrorFlags (dec)": [],
            "ErrorFlags (bin)": [],
            "ChgPackCurr": [],
            "ChgPackVolt": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (dec)": [],
            "QnovoAFC_LogVar1\nl_LoggingPath (bin)": [],
            "QnovoAFC_LogVar2\nl_InitializedFlag": [],
            "QnovoAFC_LogVar3\nl_ValidSampleFlag": [],
            "QnovoAFC_LogVar4\nl_QNS_State": [],
            "QnovoAFC_LogVar5\nl_PresentStageNum": [],
            "QnovoAFC_LogVar6\nl_HighestIndex": [],
            "QnovoAFC_LogVar7\nl_Highest_Index": [],
            "QnovoAFC_LogVar8\nl_CCCPS_Stage": [],
            "QnovoAFC_LogVar9\nl_CPVCorrIdx": [],
            "QnovoAFC_LogVar10\nl_CV_Curr": [],
            "QnovoAFC_LogVar11\nl_ProtocolStgCurr": [],
            "QnovoAFC_LogVar12\nl_PreChgCurr": [],
            "QnovoAFC_LogVar13\nl_ColdCompensatedCurr": [],
            "QnovoAFC_LogVar14\nl_CompensatedVolt": [],
            "QnovoAFC_LogVar15\nl_SampleCellVolt": [],
            "QnovoAFC_LogVar16\nl_RefCellVolt": [],
        }

        for each_time_step in all_time_steps:
            # Setup Variables
            # ------------------------------------------------
            test_filename = each_time_step["Inputs"]["Filename"]
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
            battery_state = each_time_step["Inputs"]["Battery_State"]
            lib.VeAPI_b_EVSEChgStatus = each_time_step["Inputs"]["EVSEChgStatus"]

            # Setup initial RAM
            if input_time == start_time - 1:
                lib.s_AFC_Calc.VeAFC_I_CV_Curr = each_time_step["Inputs"][
                    "logged_VeAFC_I_CV_Curr"
                ]
                lib.s_AFC_Calc.VaAFC_b_ValidSampleFlag = each_time_step["Inputs"][
                    "logged_VaAFC_b_ValidSampleFlag"
                ]
                lib.s_AFC_Calc.VaAFC_U_SampleCellVolt = each_time_step["Inputs"][
                    "logged_VaAFC_U_SampleCellVolt"
                ]
                lib.VeAFC_b_Initialized = each_time_step["Inputs"][
                    "logged_VeAFC_b_Initialized"
                ]

            if input_time > start_time - 1:
                # Setup initial RAM
                if input_time == start_time:
                    lib.s_AFC_Calc.VeAFC_e_QNS_State = each_time_step["Inputs"][
                        "logged_VeAFC_e_QNS_State"
                    ]
                    lib.s_AFC_Calc.VeAFC_Cnt_PresentStgNum = each_time_step["Inputs"][
                        "logged_VeAFC_Cnt_PresentStgNum"
                    ]

                # these could be updated at any time step due to LoadNVM and SaveNVM
                lib.s_AFC_Calc.VaAFC_Cnt_CPVCorrIdx = each_time_step["Inputs"][
                    "logged_VaAFC_Cnt_CPVCorrIdx"
                ]
                lib.s_AFC_Calc.VaAFC_U_RefCellVolt = each_time_step["Inputs"][
                    "logged_VaAFC_U_RefCellVolt"
                ]

                # Run Function
                # ------------------------------------------------
                lib.Qnovo_AFC_1000ms(
                    lib.VaAPI_Cmp_NVMRegion,
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
                    ffi.addressof(lib, "VeAFC_e_ErrorFlags"),
                    ffi.addressof(lib, "VeAFC_I_ChgPackCurr"),
                    ffi.addressof(lib, "VeAFC_U_ChgPackVolt"),
                    ffi.addressof(lib, "VeAFC_b_ChgCompletionFlag")
                )

                # Record results
                results["Filename"].append(test_filename)
                results["Time"].append(input_time)
                results["PackCurr"].append(lib.VeAPI_I_PackCurr)
                results["PackCurr_DR"].append(lib.VeAPI_b_PackCurr_DR)
                results["CellVolts"].append(lib_array_to_list(lib.VaAPI_U_CellVolts))
                results["CellVolts_DR"].append(
                    lib_array_to_list(lib.VaAPI_b_CellVolts_DR)
                )
                results["TempSnsrs"].append(lib_array_to_list(lib.VaAPI_T_TempSnsrs))
                results["TempSnsrs_DR"].append(
                    lib_array_to_list(lib.VaAPI_b_TempSnsrs_DR)
                )
                results["MinTempSnsr"].append(lib.VeAPI_T_MinTempSnsr)
                results["MinTempSnsr_DR"].append(lib.VeAPI_b_MinTempSnsr_DR)
                results["MaxTempSnsr"].append(lib.VeAPI_T_MaxTempSnsr)
                results["MaxTempSnsr_DR"].append(lib.VeAPI_b_MaxTempSnsr_DR)
                results["ChgPackCapcty"].append(lib.VeAPI_Cap_ChgPackCapcty)
                results["ChgPackCapcty_DR"].append(lib.VeAPI_b_ChgPackCapcty_DR)
                results["PackSOC"].append(lib.VeAPI_Pct_PackSOC)
                results["PackSOC_DR"].append(lib.VeAPI_b_PackSOC_DR)
                results["Battery_State"].append(battery_state)
                results["EVSEChgStatus"].append(lib.VeAPI_b_EVSEChgStatus)
                results[" "].append("")  # Divider between input and output
                results["ErrorFlags (dec)"].append(lib.VeAFC_e_ErrorFlags)
                results["ErrorFlags (bin)"].append(
                    format(lib.VeAFC_e_ErrorFlags, "032b")
                )
                results["ChgPackCurr"].append(lib.VeAFC_I_ChgPackCurr)
                results["ChgPackVolt"].append(lib.VeAFC_U_ChgPackVolt)

                results["QnovoAFC_LogVar1\nl_LoggingPath (dec)"].append(
                    lib.QnovoAFC_LogVar1
                )
                results["QnovoAFC_LogVar1\nl_LoggingPath (bin)"].append(
                    format(lib.QnovoAFC_LogVar1, "032b")
                )

                results["QnovoAFC_LogVar2\nl_InitializedFlag"].append(
                    max(0, lib.QnovoAFC_LogVar2 - CeAPI_b_LogOffsetZero)
                )

                results["QnovoAFC_LogVar3\nl_ValidSampleFlag"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar3)
                )

                results["QnovoAFC_LogVar4\nl_QNS_State"].append(
                    max(0, lib.QnovoAFC_LogVar4 - CeAFC_cmp_LogOffset)
                )
                results["QnovoAFC_LogVar5\nl_PresentStageNum"].append(
                    max(0, lib.QnovoAFC_LogVar5 - CeAFC_cmp_LogOffset)
                )
                results["QnovoAFC_LogVar6\nl_HighestIndex"].append(
                    max(0, lib.QnovoAFC_LogVar6 - CeAFC_cmp_LogOffset)
                )
                results["QnovoAFC_LogVar7\nl_Highest_Index"].append(
                    max(0, lib.QnovoAFC_LogVar7 - CeAFC_cmp_LogOffset)
                )
                results["QnovoAFC_LogVar8\nl_CCCPS_Stage"].append(
                    max(0, lib.QnovoAFC_LogVar8 - CeAFC_cmp_LogOffset)
                )
                results["QnovoAFC_LogVar9\nl_CPVCorrIdx"].append(
                    lib_array_to_list(lib.QnovoAFC_LogVar9)
                )
                results["QnovoAFC_LogVar10\nl_CV_Curr"].append(
                    max(0, lib.QnovoAFC_LogVar10 - CeAFC_I_LogOffset)
                )
                results["QnovoAFC_LogVar11\nl_ProtocolStgCurr"].append(
                    lib.QnovoAFC_LogVar11 - CeAFC_I_LogOffset
                )
                results["QnovoAFC_LogVar12\nl_PreChgCurr"].append(
                    max(0, lib.QnovoAFC_LogVar12 - CeAFC_I_LogOffset)
                )
                results["QnovoAFC_LogVar13\nl_ColdCompensatedCurr"].append(
                    max(0, lib.QnovoAFC_LogVar13 - CeAFC_I_LogOffset)
                )
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
        with open(f"{_FILENAME}_debug.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(results.keys())
            rows = zip(*results.values())
            writer.writerows(rows)
