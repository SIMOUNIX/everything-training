def bubble_sort(lst: list) -> list:
    n = len(lst)

    for i in range(n):
        for j in range(i, n):
            if lst[i] > lst[j]:
                tmp = lst[i]
                lst[i] = lst[j]
                lst[j] = tmp

    return lst
