def partitions(n):
    if n <= 0: return
    m = int((1 + sqrt(1 + 8 * n)) / 2) - 1
    p = [(1, n)]
    yield p
    while p[-1][0] != n: # or equivalently p[0][1] != 1
        rest = 0
        times, number = p.pop()
        if number == 1:
            rest += times
            times, number = p.pop()
        times -= 1
        rest += number
        if times > 0:
            p.append((times, number))
        number -= 1
        times, rest = divmod(rest, number)
        p.append((times, number))
        if rest > 0:
            p.append((1, rest))
        assert len(p) <= m # preallocation possible
        yield p
