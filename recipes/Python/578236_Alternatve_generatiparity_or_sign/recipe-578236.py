def perm_parity2(a):
    '''\
    Using algorithm from http://stackoverflow.com/questions/337664/counting-inversions-in-an-array/6424847#6424847
    But substituting Pythons in-built TimSort'''

    a = list(a)
    b = sorted(a)
    inversions = 0
    while a:
        first = a.pop(0)
        inversions += b.index(first)
        b.remove(first)
    return -1 if inversions % 2 else 1
