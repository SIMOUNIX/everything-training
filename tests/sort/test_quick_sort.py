import pytest

from src.sort.quick_sort import quick_sort


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
def test_quick_sort(lst):
    assert quick_sort(lst) == sorted(lst)
