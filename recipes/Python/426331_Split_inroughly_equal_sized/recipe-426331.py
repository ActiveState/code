def colsplit(l, cols):
    rows = len(l) / cols
    if len(l) % cols:
        rows += 1
    m = []
    for i in range(rows):
        m.append(l[i::rows])
    return m
