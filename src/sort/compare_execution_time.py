import time
from typing import Callable  # to type a function parameter

from src.sort.bubble_sort import bubble_sort
from src.sort.merge_sort import merge_sort_bottom_up, merge_sort_top_down
from src.sort.selection_sort import selection_sort

FUNCTIONS = {
    "bubble_sort": bubble_sort,
    "selection_sort": selection_sort,
    "merge_sort_top_down": merge_sort_top_down,
    "merge_sort_bottom_up": merge_sort_bottom_up,
}


def measure_execution_time(sort_function: Callable, data: list) -> float:
    start_time = time.time()
    sort_function(data)
    end_time = time.time()
    return end_time - start_time


def compare_sorting_algorithms():
    test_data = list(range(10000, 0, -1))  # a large list in descending order

    for name, function in FUNCTIONS.items():
        execution_time = measure_execution_time(function, test_data)
        print(f"{name}: {execution_time:.6f} seconds")


if __name__ == "__main__":
    compare_sorting_algorithms()
