def nprint(number, period=3, delimiter=" "):
    assert isinstance(number, (int, long)), "only integers are allowed"
    if number >= 0:
        sign = ""
    else:
        sign = "-"
        number = -number
    parts = []
    d = 10 ** period
    while number >= d:
        number, m = divmod(number, d)
        parts.insert(0, "%0*d" % (period, m))
    parts.insert(0, str(number))
    return sign + delimiter.join(parts)
