def find_close(w, h):
    PaperSizes = {                   # add new: ensure that first number is <= second number
            'A0': [2384, 3370],
            'A1': [1684, 2384],
            'A2': [1190, 1684],
            'A3': [842, 1190],
            'A4': [595, 842],
            'A5': [420, 595],
            'A6': [298, 420],
            'A7': [210, 298],
            'A8': [148, 210],
            'B0': [2835, 4008],
            'B1': [2004, 2835],
            'B2': [1417, 2004],
            'B3': [1001, 1417],
            'B4': [709, 1001],
            'B5': [499, 709],
            'B6': [354, 499],
            'B7': [249, 354],
            'B8': [176, 249],
            'B9': [125, 176],
            'B10': [88, 125],
            'C2': [1837, 578],
            'C3': [578, 919],
            'C4': [919, 649],
            'C5': [649, 459],
            'C6': [459, 323],
            'Invoice': [396, 612],
            'Executive': [522, 756],
            'Letter': [612, 792],
            'Legal': [612, 1008],
            'Ledger': [792, 1224],
            }

    wi = int(round(w, 0))
    hi = int(round(h, 0))
    if w <= h:
        w1 = wi
        h1 = hi
    else:
        w1 = hi
        h1 = wi

    sw = str(w1)
    sh = str(h1)
    stab = [abs(w1-s[0])+abs(h1-s[1]) for s in PaperSizes.values()]
    small = min(stab)
    idx = stab.index(small)
    f = PaperSizes.keys()[idx]

    if w <= h:
        ff = f + "-P"
        ss = str(PaperSizes[f][0]) + " x " + str(PaperSizes[f][1])
    else:
        ff = f + "-L"
        ss = str(PaperSizes[f][1]) + " x " + str(PaperSizes[f][0])

    if small == 0:                # exact fit
        return ff
    rtxt = "%s x %s (other), closest: %s = %s"   # else show best fit
    rtxt = rtxt % (sw, sh, ff, ss)
    return rtxt
