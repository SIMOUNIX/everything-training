# shorten a list reprenstation by grouping the same following letters
# ex: QQQQQQQQQWWEEER -> 9Q2W3E1R (15 to 9 characters)

# this implementation is not handeling all the edge cases such as numbers in the original sequence
# a future implementaion will be done to remove the problem

def naive_reduce_list(input_str: str) -> str:
    res = ""
    total_len = len(input_str)
    i = 0
    acc = 1

    # double while to process the total sentence and then the inner same characters sequence
    while i < total_len - 1:
        if input_str[i] == input_str[i + 1]:
            acc += 1
        else:
            res += str(acc)
            res += input_str[i - 1]
            acc = 1
        i += 1
    return res
