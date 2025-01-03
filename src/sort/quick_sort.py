# how quick sort works:
# 1. choose a pivot element from the list
# 2. partition the list into two sublists: elements less than the pivot and elements greater than the pivot
# 3. recursively apply quick sort to the two sublists
# 4. combine the sorted sublists and the pivot element
# 5. the base case is when the input list is empty or has only one element
# uses recursion and divide-and-conquer strategy


def quick_sort(lst: list) -> list:
    n = len(lst)
    if n <= 1:
        return lst

    # pivot is the middle element
    pivot = lst[n // 2]

    # store in left all the elements that are lower than the pivot
    left = [x for x in lst if x < pivot]

    # store in middle all the elements that are equal to the pivot in case of duplicates
    middle = [x for x in lst if x == pivot]

    # store in right all the elements that are greater than the pivot
    right = [x for x in lst if x > pivot]

    # recursively apply quick sort to the two sublists
    return quick_sort(left) + middle + quick_sort(right)
