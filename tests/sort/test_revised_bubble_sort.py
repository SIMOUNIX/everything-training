from sort.revised_bubble_sort import revised_bubble_sort


def test_revised_bubble_sort_empty_list():
    assert revised_bubble_sort([]) == []


def test_revised_bubble_sort_single_element_list():
    assert revised_bubble_sort([1]) == [1]


def test_revised_bubble_sort_negative_list():
    assert revised_bubble_sort([-1, -2, -3]) == [-3, -2, -1]


def test_revised_bubble_sort_random_list():
    assert revised_bubble_sort([5, 3, 8, 6, 2]) == [2, 3, 5, 6, 8]


def test_revised_bubble_sort_character_list():
    assert revised_bubble_sort(["a", "c", "b"]) == ["a", "b", "c"]


def test_revised_bubble_sort_string_list():
    assert revised_bubble_sort(["simon", "adrien", "lea"]) == [
        "adrien",
        "lea",
        "simon",
    ]


def test_revised_bubble_sort_same_string():
    assert revised_bubble_sort(["adrien", "simon", "adrien", "lea"]) == [
        "adrien",
        "adrien",
        "lea",
        "simon",
    ]
