from sort.selection_sort import selection_sort


def test_selection_sort_empty_list():
    assert selection_sort([]) == []


def test_selection_sort_single_element_list():
    assert selection_sort([1]) == [1]


def test_selection_sort_negative_list():
    assert selection_sort([-1, -2, -3]) == [-3, -2, -1]


def test_selection_sort_random_list():
    assert selection_sort([5, 3, 8, 6, 2]) == [2, 3, 5, 6, 8]


def test_selection_sort_character_list():
    assert selection_sort(["a", "c", "b"]) == ["a", "b", "c"]


def test_selection_sort_string_list():
    assert selection_sort(["simon", "adrien", "lea"]) == [
        "adrien",
        "lea",
        "simon",
    ]


def test_selection_sort_same_string():
    assert selection_sort(["adrien", "simon", "adrien", "lea"]) == [
        "adrien",
        "adrien",
        "lea",
        "simon",
    ]


def test_selection_sort_already_sorted():
    assert selection_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_selection_sort_large_list():
    large_list = list(range(1000, 0, -1))  # descending order
    assert selection_sort(large_list) == list(range(1, 1001))  # ascending order
