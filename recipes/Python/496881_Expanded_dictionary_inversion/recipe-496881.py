def invert1(d):
    dd = {}
    for k, v in d.items():
        if not isinstance(v, (tuple, list)): v = [v]
        dd.update( [(vv, dd.setdefault(vv, []) + [k]) for vv in v] )
    return dd


def invert2(d):
    dd = {}
    for k, v in d.items():
        if not isinstance(v, (tuple, list)): v = [v]
        [dd.setdefault(vv, []).append(k) for vv in v]
    return dd
