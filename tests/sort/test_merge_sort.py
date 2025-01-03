import pytest

from src.sort.merge_sort import (
    merge,
    merge_sort_bottom_up,
    merge_sort_top_down,
)


# merge behavior, check if the two lists are merged in ascending order
@pytest.mark.parametrize(
    "lst1, lst2, expected",
    [
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3], [], [1, 2, 3]),
        ([], [4, 5, 6], [4, 5, 6]),
        ([1, 1, 1], [1, 1], [1, 1, 1, 1, 1]),
        ([1], [2], [1, 2]),
    ],
)
def test_merge(lst1, lst2, expected):
    assert merge(lst1, lst2) == expected


@pytest.mark.parametrize(
    "lst",
    [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 3, 8, 6, 2, 7, 4, 1],
        [10, -1, 3, 2, 5, 0, -2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
    ],
)
def test_merge_sort_bottom_up(lst):
    # sorted() is the built-in Python function that returns a sorted list
    assert merge_sort_bottom_up(lst) == sorted(lst)


@pytest.mark.parametrize(
    "lst",
    [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 3, 8, 6, 2, 7, 4, 1],
        [10, -1, 3, 2, 5, 0, -2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
    ],
)
def test_merge_sort_top_down(lst):
    assert merge_sort_top_down(lst) == sorted(lst)


@pytest.mark.parametrize(
    "lst",
    [
        [5, 3, 8, 6, 2, 7, 4, 1],
        [10, -1, 3, 2, 5, 0, -2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
    ],
)
def test_consistency_between_sorting_algorithms(lst):
    assert merge_sort_bottom_up(lst) == merge_sort_top_down(lst)
