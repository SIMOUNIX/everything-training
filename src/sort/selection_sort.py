# selection sort works by selecting the smallest element from the unsorted portion of the list
# and swapping it with the first element of the unsorted portion of the list


def selection_sort(lst: list) -> list:
    n = len(lst)

    for i in range(n):
        # assume the first element is the smallest
        # from the unsorted portion of the list
        min_index = i

        # find the smallest element from the unsorted portion of the list
        for j in range(i + 1, n):
            if lst[j] < lst[min_index]:
                min_index = j

        # swap the smallest element with the first element of the unsorted portion of the list
        lst[i], lst[min_index] = lst[min_index], lst[i]

    return lst


# example of how it works
# lst = [5, 3, 8, 6, 2]
# 1st iteration:
#   - min_index = 0
#   - 2 < 5, so min_index = 4
#   - swap 5 and 2
#   - lst = [2, 3, 8, 6, 5]
# 2nd iteration:
#   - min_index = 1
#   - 3 < 8, so min_index = 1
#   - swap 8 and 3
#   - lst = [2, 3, 8, 6, 5]
# and so on
