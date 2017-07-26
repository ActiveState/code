def group(a, *ns):
    for n in ns:
        a = [a[i:i+n] for i in xrange(0, len(a), n)]
    return a

def join(a, *cs):
    return [cs[0].join(join(t, *cs[1:])) for t in a] if cs else a

def hexdump(data):
    toHex = lambda c: '{:02X}'.format(ord(c))
    toChr = lambda c: c if 32 <= ord(c) < 127 else '.'
    make = lambda f, *cs: join(group(map(f, data), 8, 2), *cs)
    hs = make(toHex, '  ', ' ')
    cs = make(toChr, ' ', '')
    for i, (h, c) in enumerate(zip(hs, cs)):
        print '{:010X}: {:48}  {:16}'.format(i * 16, h, c)
