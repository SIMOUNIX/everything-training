from sort.bubble_sort import bubble_sort


def test_bubble_sort_empty_list():
    assert bubble_sort([]) == []


def test_bubble_sort_single_element_list():
    assert bubble_sort([1]) == [1]


def test_bubble_sort_negative_list():
    assert bubble_sort([-1, -2, -3]) == [-3, -2, -1]


def test_bubble_sort_random_list():
    assert bubble_sort([5, 3, 8, 6, 2]) == [2, 3, 5, 6, 8]


def test_bubble_sort_character_list():
    assert bubble_sort(["a", "c", "b"]) == ["a", "b", "c"]


def test_bubble_sort_string_list():
    assert bubble_sort(["simon", "adrien", "lea"]) == [
        "adrien",
        "lea",
        "simon",
    ]
