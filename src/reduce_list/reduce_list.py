# more advanced reduce list
# ex of output:
# QQQQQQQQQWWEEER -> 9\Q2\W3\E1\R
# when dealing with backslashes
# QQQQQQ\\\\::: -> 6\Q4\\3\:

def reduce_list(input_str: str) -> str:
    if not input_str:
        return ""

    res = ""
    total_len = len(input_str)
    acc = 1

    # double while to process the total sentence and then the inner same characters sequence
    for i in range(1, total_len):
        if input_str[i] == input_str[i - 1]:
            acc += 1
        else:
            res += str(acc)
            res += str("\\")
            res += input_str[i - 1]
            acc = 1

    res += str(acc) + str("\\") + input_str[i - 1]

    return res

print(reduce_list("QQQQQQ\\\\:::"))
