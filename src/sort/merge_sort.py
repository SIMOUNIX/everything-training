# see: https://en.wikipedia.org/wiki/Merge_sort for more information
# I will implement the bottom up and top down merge sort algorithms
# comparing the efficiency of the two algorithms


# bottom up merge advantages:
# - no recursion
# - easy to implement


def merge(lst1: list, lst2: list) -> list:
    result = []
    i = j = 0

    # merge list in ascending order
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            result.append(lst1[i])
            i += 1
        else:
            result.append(lst2[j])
            j += 1

    # add the remaining elements, should be greater than the rest
    result.extend(lst1[i:])
    result.extend(lst2[j:])

    return result


def merge_sort_bottom_up(lst: list) -> list:
    n = len(lst)
    if n <= 1:
        return lst

    # split the list into sublists of size 1
    sublists = [[lst[i]] for i in range(n)]
    # print(f"Initial sublists: {sublists}")

    # iteration = 0

    # merge the sublists
    # we go until there is only one sublist left -> the sorted list
    while len(sublists) > 1:
        # iteration += 1
        # print(f"\nIteration {iteration}:")
        new_sublists = []
        for i in range(0, len(sublists), 2):
            # if there are two sublists to merge
            if i + 1 < len(sublists):
                merged = merge(sublists[i], sublists[i + 1])
                # print(f"Merging {sublists[i]} and {sublists[i + 1]} -> {merged}")
                new_sublists.append(merged)
            else:  # odd number of sublists
                # print(f"Single sublist {sublists[i]} remains unchanged")
                new_sublists.append(sublists[i])
        sublists = new_sublists
        # print(f"Sublists after iteration {iteration}: {sublists}")

    return sublists[0]


def merge_sort_top_down(lst: list) -> list:
    n = len(lst)
    if n <= 1:
        return lst

    # split the list into two halves
    mid = n // 2
    left = lst[:mid]
    right = lst[mid:]

    # sort the two halves
    left = merge_sort_top_down(left)
    right = merge_sort_top_down(right)

    return merge(left, right)


# FUTURE WORKS:
# see the in place merge sort algorithm
# the biggest drawback of merge sort is the space complexity
# the in place merge sort algorithm is a way to reduce the space complexity
