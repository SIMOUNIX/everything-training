# bubble sort still compare all the elements in the list even though the list is already sorted
# in the revised version we add a flag if any swap is made in the inner loop


def revised_bubble_sort(lst: list) -> list:
    n = len(lst)

    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True

        # if no two elements were swapped in the inner loop, then the list is already sorted
        if not swapped:
            break

    return lst
