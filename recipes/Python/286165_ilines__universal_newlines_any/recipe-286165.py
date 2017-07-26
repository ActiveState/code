def ilines(source_iterable):
    '''yield lines as in universal-newlines from a stream of data blocks'''
    tail = ''
    for block in source_iterable:
        if not block:
            continue
        if tail.endswith('\015'):
            yield tail[:-1] + '\012'
            if block.startswith('\012'):
                pos = 1
            else:
                tail = ''
        else:
            pos = 0
        try:
            while True: # While we are finding LF.
                npos = block.index('\012', pos) + 1
                try:
                    rend = npos - 2
                    rpos = block.index('\015', pos, rend)
                    if pos:
                        yield block[pos : rpos] + '\n'
                    else:
                        yield tail + block[:rpos] + '\n'
                    pos = rpos + 1
                    while True: # While CRs 'inside' the LF
                        rpos = block.index('\015', pos, rend)
                        yield block[pos : rpos] + '\n'
                        pos = rpos + 1
                except ValueError:
                    pass
                if '\015' == block[rend]:
                    if pos:
                        yield block[pos : rend] + '\n'
                    else:
                        yield tail + block[:rend] + '\n'
                elif pos:
                    yield block[pos : npos]
                else:
                    yield tail + block[:npos]
                pos = npos
        except ValueError:
            pass
        # No LFs left in block.  Do all but final CR (in case LF)
        try:
            while True:
                rpos = block.index('\015', pos, -1)
                if pos:
                    yield block[pos : rpos] + '\n'
                else:
                    yield tail + block[:rpos] + '\n'
                pos = rpos + 1
        except ValueError:
            pass

        if pos:
            tail = block[pos:]
        else:
            tail += block
    if tail:
        yield tail
