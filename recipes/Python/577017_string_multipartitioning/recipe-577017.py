def mpartition(s, *substrings):
    idx = 0
    splits = [0, None]
    for substring in substrings:
        idx = s.find(substring, idx)
        if idx == -1:
            raise ValueError, "Substring %r not found" % substring
        splits[-1:-1] = [idx, idx+len(substring)]
    return [s[splits[i]:splits[i+1]] for i in range(len(splits)-1)]
