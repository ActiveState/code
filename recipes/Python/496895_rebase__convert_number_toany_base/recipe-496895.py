import string

def rebase(i, frombase=None, tobase=None, fromalphabet=None, toalphabet=None, resize=1, too_big=40000, debug=False):
    ''' if frombase is not specified, it is guessed from the type and/or char in i with highest ord.
        tobase defaults to [10, 2][frombase == 10].
        the alphabets are map(chr, range(256)) if its base is between 62 and 255;
        otherwise, string.digits+string.letters.
        always returns a string which is also valid input.
        valid bases are ints in range(-256, 257).
        alphabets must be subscriptable, and can only contain str's.
        invalid tobases are replied with 'why?'; rebase('why?') == '217648673'.
        returned string is zfilled to the next largest multiple of resize
    '''
    if frombase == None:
        if isinstance(i, (int, long)):
            frombase = 10
        elif isinstance(i, str):
            a = str(i)
            if any([(chr(x) in a) for x in range(ord('0')) + range(58, 65) + range(91, 97) + range(123, 256)]):
                frombase = max(map(ord, a)) + 1
            else:
                frombase = max(map((string.digits + string.letters).index, a)) + 1
    if tobase == None:
        tobase = [10, 2][frombase == 10]
    # got bases, ensuring that everything is an int
    tobase = int(tobase)
    frombase = int(frombase)
    abstobase = abs(tobase)
    absfrombase = abs(frombase)
    if absfrombase in [0, 1]:
        i = len(str(i))
    elif 2 <= frombase <= 36:
        # may be difficult to translate to C
        i = int(str(i), frombase)
    else:
        i = str(i)
        n = 0
        if fromalphabet == None:
            if 62 <= absfrombase <= 256:
                fromalphabet = map(chr, range(256))
            else:
                fromalphabet = string.digits + string.letters
        fromalphabet = fromalphabet[:absfrombase]
        for j in range(len(i)):
            n += (frombase ** j) * fromalphabet.index(i[-1-j])
        i = n
    # got ints, converting to tobase
    if debug: print 'converting %d from base %d to %d' % (i, frombase, tobase)
    if abstobase in [0, 1]:
        return '0' * ((i > 0) and int(i) or 0)
    elif abstobase > 256:
        return 'why?'
    # if execution gets here, we might want the result to be zfilled to a multiple of resize
    r = ''
    if tobase == 10:
        r = str(i)
    else:
        if i < 0:
            print 'negative',
            i = -i
        if toalphabet is None:
            if 62 <= abstobase <= 256:
                toalphabet = map(chr, range(abstobase))
            else:
                toalphabet = (string.digits + string.letters)[:abstobase]
        if tobase < 0:
            i = -i
        j = 0
        while i != 0:
            r = toalphabet[i % tobase] + r
            i /= tobase
            j += 1
            if j >= too_big: raise "call again; set too_big bigger"
    if resize > 1:
        if 62 <= abstobase <= 256:
            r = toalphabet[0] * (resize - (len(r) % resize)) + r
        else:
            r = r.zfill(len(r) + resize - (len(r) % resize))
    return r
