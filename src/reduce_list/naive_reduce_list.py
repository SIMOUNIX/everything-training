# shorten a list reprenstation by grouping the same following letters
# ex: QQQQQQQQQWWEEER -> 9Q2W3E1R (15 to 9 characters)

# this implementation is not handeling all the edge cases such as numbers in the original sequence
# a future implementaion will be done to remove the problem

def naive_reduce_list(input_str: str) -> str:
    if not input_str:
        return ""

    res = ""
    total_len = len(input_str)
    acc = 1

    for i in range(1, total_len):
        if input_str[i] == input_str[i - 1]:
            acc += 1
        else:
            res += str(acc)
            res += input_str[i - 1]
            acc = 1

    # add the last character to the final string
    res += str(acc) + input_str[-1]
    return res
