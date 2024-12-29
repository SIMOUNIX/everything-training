import pytest

from reduce_list.reduce_list import reduce_list


# use of pytest.mark.parametrize to test multiple inputs
# pytest.mark.parametrize is used to shorten the test code by providing multiple inputs and expected outputs
# using a single test function
@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("", ""),
        ("a", "1\\a"),
        ("1", "1\\1"),
        ("11", "2\\1"),
        ("AAAAAAABBBCCDAA", "7\\A3\\B2\\C1\\D2\\A"),
        (
            r"QQQQQQ\\\\:::",  # r means raw string to avoid escaping the backslashes
            "6\\Q4\\\\3\\:",
        ),
    ],
)
def test_reduce_list(input_str, expected):
    assert reduce_list(input_str) == expected
