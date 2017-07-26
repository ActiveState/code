def num_in_base(val, base, min_digits=1, complement=False,
                digits="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """Convert number to string in specified base
    
       If minimum number of digits is specified, pads result to at least
       that length.
       If complement is True, prints negative numbers in complement
       format based on the specified number of digits.
       Non-standard digits can be used. This can also allow bases greater
       than 36.
    """
    if base < 2: raise ValueError("Minimum base is 2")
    if base > len(digits): raise ValueError("Not enough digits for base")
    # Deal with negative numbers
    negative = val < 0
    val = abs(val)
    if complement:
        sign = ""
        max = base**min_digits
        if (val > max) or (not negative and val == max):
            raise ValueError("Value out of range for complemented format")
        if negative:
            val = (max - val)
    else:
        sign = "-" * negative
    # Calculate digits
    val_digits = []
    while val:
        val, digit = divmod(val, base)
        val_digits.append(digits[digit])
    result = "".join(reversed(val_digits))
    leading_digits = (digits[0] * (min_digits - len(result)))
    return sign + leading_digits + result

if __name__ == "__main__":
    # Quick sanity check
    for base in range(2, 37):
        for val in range(-1000, 1000):
            assert val == int(num_in_base(val, base), base)

    # Quick sanity check of complemented format
    def comp(val, base, digits):
        return num_in_base(val, base, digits, complement = True)
    for base in range(2, 37):
        for digits in range(1, 11):
            limit = base ** digits
            for val in range(-min(limit, 1000), 0):
                assert limit + val == int(comp(val, base, digits), base)
            for val in range(0, min(limit, 1000)):
                assert val == int(comp(val, base, digits), base)
