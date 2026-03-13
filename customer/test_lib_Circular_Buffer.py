from .__main__ import *


SKIP_MODULE = False  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 6,
                    "max_num_elements": 10,
                },
                "Expected": {
                    "expected_buffer": [0 for _ in range(10)],
                    "result": 0,
                    "max_num_elements": 10,
                    "element_size": 6,
                    "num_elements_inserted": 0,
                },
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Intialize the handler of Generic circular buffer implementation: "
                    "element_size 6, num_elements_inserted : 0"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 0,
                    "max_num_elements": 0,
                },
                "Expected": {
                    "expected_buffer": [0 for _ in range(10)],
                    "result": 0,
                    "max_num_elements": 0,
                    "element_size": 0,
                    "num_elements_inserted": 0,
                },
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Intialize the handler of Generic circular buffer implementation,"
                    "element_size 0, num_elements_inserted 0"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "handle": None,
                    "element_size": 6,
                    "max_num_elements": 10,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Intialize the handler of Generic circular buffer implementation, handle NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [],
                    "element_size": 6,
                    "max_num_elements": 10,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "Intialize the handler of Generic circular buffer implementation, Buffer NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_init(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of initialization of circular buffer.
    Intialize the handler of Generic circular buffer implementation
    """

    set_lib_inputs(lib, test_cases)
    #ffi.addressof(lib, "buff"),
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        expected = test_cases["Expected"]["result"]
        actual_r = lib.LIB_CircBuffInit(
            ffi.NULL,
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        compare_result(expected, actual)
    elif "buff" in test_cases["Inputs"]:
        if test_cases["Inputs"]["buff"] is []:
            expected = test_cases["Expected"]["result"]
            actual = lib.LIB_CircBuffInit(
                ffi.addressof(lib, "Input_CircBuffHandle_t"),
                ffi.NULL,
                test_cases["Inputs"]["element_size"],
                test_cases["Inputs"]["max_num_elements"],
            )
            compare_result(expected, actual)
    else:
        actual = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            ffi.addressof(lib, "buff"),
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
        buffer_data = list(
            ffi.buffer(
                lib.Input_CircBuffHandle_t.buff_addr,
                test_cases["Inputs"]["buff_size"],
            )
        )
        buffer_data_int = [int.from_bytes(x, byteorder="big") for x in buffer_data]
        expected = test_cases["Expected"]["expected_buffer"]
        actual = buffer_data_int

        print(f"Expected: {expected}")
        print(f"Actual: {actual}")

        compare_result(expected, actual, compare_all_elements=True)

        expected = test_cases["Expected"]["num_elements_inserted"]
        actual = lib.Input_CircBuffHandle_t.num_elements_inserted
        compare_result(expected, actual)
        expected = 0
        actual = lib.Input_CircBuffHandle_t.next_element_position
        compare_result(expected, actual)
        expected = test_cases["Expected"]["max_num_elements"]
        actual = lib.Input_CircBuffHandle_t.max_num_elements
        compare_result(expected, actual)

        expected = test_cases["Expected"]["element_size"]
        actual = lib.Input_CircBuffHandle_t.element_size
        compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                },
                "Expected": {
                    "expected_buffer": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                },
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Generic circular buffer Insertion exact buffer elements"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "ele_arr_overflow_1": [5, 6],
                },
                "Expected": {
                    "expected_buffer": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                    "expected_overflow_buffer_1": [5, 6, 5, 6, 1, 2, 1, 2, 1, 2],
                },
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Generic circular buffer implementation, buffer exceed max elements"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "handle": None,
                    "element_size": 6,
                    "max_num_elements": 10,
                    "ele_arr": [1, 2],
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_3",
            marks=[
                mark.description("Generic circular buffer implementation, handle NULL"),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [],
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_4",
            marks=[
                mark.description(
                    "Generic circular buffer implementation, element array null"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 2,
                    "ele_arr": [1, 2],
                },
                "Expected": {
                    "expected_buffer": [1, 2, 1, 2, 0, 0, 0, 0, 0, 0],
                },
            },
            id="Test_Case_5",
            marks=[
                mark.description(
                    "Generic circular buffer implementation, buffer < max elements"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 20,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "element_size_less": True,
                    "ele_arr_overflow_2": [5, 6],
                },
                "Expected": {
                    "expected_buffer": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                    "expected_buffer_1": [5, 6, 5, 6, 1, 2, 1, 2, 1, 2],
                },
            },
            id="Test_Case_6",
            marks=[
                mark.description(
                    "Generic circular buffer implementation, buffer size > max element size"
                ),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_insert(lib, setup_parameters, test_cases) -> None:
    """
    This test function performs verification of insertion of items to circular buffer
    """

    set_lib_inputs(lib, test_cases)
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        actual_r = lib.LIB_CircBuffInsert(ffi.NULL, lib.ele_arr)
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    elif "ele_arr" in test_cases["Inputs"] and test_cases["Inputs"]["ele_arr"] == []:
        lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual_r = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            ffi.NULL,
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    else:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )

        actual = int.from_bytes(actual_r, byteorder='little', signed=True)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        expected = test_cases["Expected"]["expected_buffer"]
        buffer_data = list(
            ffi.buffer(
                lib.Input_CircBuffHandle_t.buff_addr,
                test_cases["Inputs"]["buff_size"],
            )
        )
        actual = [int.from_bytes(x, byteorder="big") for x in buffer_data]
        print(f"Actual: {actual}")
        compare_result(expected, actual)

        if "ele_arr_overflow_1" in test_cases["Inputs"]:
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_1
            )
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_1
            )

            expected = test_cases["Expected"]["expected_overflow_buffer_1"]
            buffer_data = list(
                ffi.buffer(
                    lib.Input_CircBuffHandle_t.buff_addr,
                    test_cases["Inputs"]["buff_size"],
                )
            )
            actual = [int.from_bytes(x, byteorder="big") for x in buffer_data]
            compare_result(expected, actual)
        if "element_size_greater" in test_cases["Inputs"]:
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_2
            )
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_2
            )
            expected = test_cases["Expected"]["expected_buffer_1"]
            buffer_data = list(
                ffi.buffer(
                    lib.Input_CircBuffHandle_t.buff_addr,
                    test_cases["Inputs"]["buff_size"],
                )
            )
            actual = [int.from_bytes(x, byteorder="big") for x in buffer_data]
            print(f"Actual : Element Size Greater: {actual}")
            compare_result(expected, actual)
        if "element_size_less" in test_cases["Inputs"]:
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_2
            )
            result = lib.LIB_CircBuffInsert(
                ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_2
            )
            expected = test_cases["Expected"]["expected_buffer_1"]
            buffer_data = list(
                ffi.buffer(
                    lib.Input_CircBuffHandle_t.buff_addr,
                    test_cases["Inputs"]["buff_size"],
                )
            )
            actual = [int.from_bytes(x, byteorder="big") for x in buffer_data]
            print(f"Actual : Element Size less: {actual}")
            compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "handle": None,
                    "is_buff_full": ffi.new("unsigned char *"),
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is full, handle NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 6,
                    "max_num_elements": 10,
                    "is_buff_full": ffi.new("unsigned char *"),
                    "buff_check_nullptr": True,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is full, buffer check pointer NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "is_buff_full": ffi.new("unsigned char *"),
                    "buff_check_full": True,
                },
                "Expected": {"result_1": 0, "result_2": 1},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is full, buffer not full, full scenarios"
                ),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_is_full(lib, setup_parameters, test_cases) -> None:
    """
    Generic circular buffer check if buffer is full
    """

    set_lib_inputs(lib, test_cases)
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        actual_r = lib.LIB_CircBuffIsFull(ffi.NULL, lib.is_buff_full)
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    elif "buff_check_nullptr" in test_cases["Inputs"]:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual_r = lib.LIB_CircBuffIsFull(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), ffi.NULL
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)

    elif "buff_check_full" in test_cases["Inputs"]:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )

        result = lib.LIB_CircBuffIsFull(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.is_buff_full
        )
        expected = test_cases["Expected"]["result_1"]
        actual = lib.is_buff_full[0]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffIsFull(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.is_buff_full
        )
        expected = test_cases["Expected"]["result_2"]
        actual = lib.is_buff_full[0]
        compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "handle": None,
                    "is_buff_empty": ffi.new("unsigned char *"),
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is empty, handle NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 6,
                    "max_num_elements": 10,
                    "is_buff_empty": ffi.new("unsigned char *"),
                    "buff_check_nullptr": True,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is empty, buffer check pointer NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "is_buff_empty": ffi.new("unsigned char *"),
                    "buff_check_empty": True,
                },
                "Expected": {"result_1": 1, "result_2": 0},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Generic circular buffer check if buffer is empty, empty, not empty scenarios"
                ),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_is_empty(lib, setup_parameters, test_cases) -> None:
    """
    Generic circular buffer check if buffer is empty
    """

    set_lib_inputs(lib, test_cases)
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        actual_r = lib.LIB_CircBuffIsFull(ffi.NULL, lib.is_buff_full)
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    elif "buff_check_nullptr" in test_cases["Inputs"]:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual_r = lib.LIB_CircBuffIsEmpty(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), ffi.NULL
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)

    elif "buff_check_empty" in test_cases["Inputs"]:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        result = lib.LIB_CircBuffIsEmpty(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.is_buff_empty
        )
        expected = test_cases["Expected"]["result_1"]
        actual = lib.is_buff_empty[0]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffIsEmpty(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.is_buff_empty
        )
        expected = test_cases["Expected"]["result_2"]
        actual = lib.is_buff_empty[0]
        compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "handle": None,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_1",
            marks=[
                mark.description(
                    "Generic circular buffer get number of elements inserted, handle NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 6,
                    "max_num_elements": 10,
                    "buff_check_nullptr": True,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Generic circular buffer get number of elements inserted, check pointer NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "num_elements_inserted": ffi.new("unsigned short *"),
                },
                "Expected": {"result_1": 0, "result_2": 1, "result_3": 5},
            },
            id="Test_Case_3",
            marks=[
                mark.description(
                    "Generic circular buffer get number of elements inserted, coverage"
                ),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_num_elements_inserted(
    lib, setup_parameters, test_cases
) -> None:
    """
    Generic circular buffer get number of elements inserted,
    """

    set_lib_inputs(lib, test_cases)
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        actual_r = lib.LIB_CircBuffIsFull(ffi.NULL, lib.is_buff_full)
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    elif "buff_check_nullptr" in test_cases["Inputs"]:
        actual = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual_r = lib.LIB_CircBuffNumElementsInserted(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), ffi.NULL
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)

    else:
        actual_r = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        result = lib.LIB_CircBuffNumElementsInserted(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.num_elements_inserted
        )
        expected = test_cases["Expected"]["result_1"]
        actual = lib.num_elements_inserted[0]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffNumElementsInserted(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.num_elements_inserted
        )
        expected = test_cases["Expected"]["result_2"]
        actual = lib.num_elements_inserted[0]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )

        result = lib.LIB_CircBuffNumElementsInserted(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.num_elements_inserted
        )
        expected = test_cases["Expected"]["result_3"]
        actual = lib.num_elements_inserted[0]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )

        result = lib.LIB_CircBuffNumElementsInserted(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.num_elements_inserted
        )
        expected = test_cases["Expected"]["result_3"]
        actual = lib.num_elements_inserted[0]
        compare_result(expected, actual)


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "handle": None,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_1",
            marks=[
                mark.description("Generic circular buffer get element, handle NULL"),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 6,
                    "max_num_elements": 10,
                    "buff_check_nullptr": True,
                },
                "Expected": {"result": -1},
            },
            id="Test_Case_2",
            marks=[
                mark.description(
                    "Generic circular buffer get element, check pointer NULL"
                ),
                mark.jira_id("TEST"),
            ],
        ),
        param(
            {
                "Inputs": {
                    "buff": [[0 for _ in range(10)] for _ in range(10)],
                    "buff_size": 10,
                    "element_size": 2,
                    "max_num_elements": 5,
                    "ele_arr": [1, 2],
                    "ele_arr_overflow_1": [5, 6],
                    "ele_index": 1,
                    "ele_addr_buff": ffi.new("unsigned char *"),
                },
                "Expected": {"result_1": [1, 2], "result_2": [5, 6]},
            },
            id="Test_Case_3",
            marks=[
                mark.description("Generic circular buffer get element, coverage"),
                mark.jira_id("TEST"),
            ],
        ),
    ],
)

def test_lib_circular_buffer_get_element(lib, setup_parameters, test_cases) -> None:
    """
    Generic circular buffer get element
    """

    set_lib_inputs(lib, test_cases)
    pointer_to_array = ffi.cast("unsigned char *", lib.buff)
    if "handle" in test_cases["Inputs"] and test_cases["Inputs"]["handle"] is None:
        actual_r = lib.LIB_CircBuffGetElement(ffi.NULL, lib.ele_index, lib.ele_addr_buff)
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)
    elif "buff_check_nullptr" in test_cases["Inputs"]:
        actual = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        actual_r = lib.LIB_CircBuffGetElement(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_index, ffi.NULL
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result"]
        compare_result(expected, actual)

    else:
        actual = lib.LIB_CircBuffInit(
            ffi.addressof(lib, "Input_CircBuffHandle_t"),
            pointer_to_array,
            test_cases["Inputs"]["element_size"],
            test_cases["Inputs"]["max_num_elements"],
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        actual_r = lib.LIB_CircBuffGetElement(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), 0, lib.ele_addr_buff
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result_1"]
        actual = [lib.ele_addr_buff[0], lib.ele_addr_buff[1]]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_1
        )
        actual = lib.LIB_CircBuffGetElement(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), 1, lib.ele_addr_buff
        )

        expected = test_cases["Expected"]["result_1"]
        actual = [lib.ele_addr_buff[0], lib.ele_addr_buff[1]]
        compare_result(expected, actual)
        actual_r = lib.LIB_CircBuffGetElement(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), 0, lib.ele_addr_buff
        )
        actual = int.from_bytes(actual_r, byteorder='little', signed=True)
        expected = test_cases["Expected"]["result_2"]
        actual = [lib.ele_addr_buff[0], lib.ele_addr_buff[1]]
        compare_result(expected, actual)

        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr
        )
        result = lib.LIB_CircBuffInsert(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), lib.ele_arr_overflow_1
        )

        actual = lib.LIB_CircBuffGetElement(
            ffi.addressof(lib, "Input_CircBuffHandle_t"), 0, lib.ele_addr_buff
        )

        expected = test_cases["Expected"]["result_2"]
        actual = [lib.ele_addr_buff[0], lib.ele_addr_buff[1]]
        compare_result(expected, actual)
