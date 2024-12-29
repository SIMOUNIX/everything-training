from reduce_list.naive_reduce_list import naive_reduce_list


def test_naive_reduce_list_empty_list():
    assert naive_reduce_list("") == ""


def test_naive_reduce_list_single_element_list():
    assert naive_reduce_list("a") == "1a"


def test_naive_reduce_list_single_element_integer_list():
    assert naive_reduce_list("1") == "11"


def test_naive_reduce_list_two_integer_list():
    assert naive_reduce_list("11") == "21"


def test_naive_reduce_list_multiple_element():
    assert naive_reduce_list("AAAAAAABBBCCDAA") == "7A3B2C1D2A"
