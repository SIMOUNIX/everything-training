import time
from typing import Callable

from src.sort.bubble_sort import bubble_sort
from src.sort.selection_sort import selection_sort


def measure_execution_time(sort_function: Callable, data: list) -> float:
    start_time = time.time()
    sort_function(data)
    end_time = time.time()
    return end_time - start_time


def compare_sorting_algorithms():
    # Generate test data
    test_data = list(range(10000, 0, -1))  # a large list in descending order

    selection_time = measure_execution_time(selection_sort, test_data.copy())
    print(f"Selection Sort Execution Time: {selection_time:.6f} seconds")

    bubble_time = measure_execution_time(bubble_sort, test_data.copy())
    print(f"Bubble Sort Execution Time: {bubble_time:.6f} seconds")


if __name__ == "__main__":
    compare_sorting_algorithms()
    # should output a factor 2 difference in execution time
