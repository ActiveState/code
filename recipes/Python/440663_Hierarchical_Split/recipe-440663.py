def nestedSplit(astring, sep=None, *subsep):
    """nestedSplit(astring, sep=None, *subsep): given astring, and one or more split
    strings, it splits astring hierarchically. The first split key is the higher level one.
    Ex.: nestedSplit("a b\nc d", "\n", " ") => [['a', 'b'], ['c', 'd']] """
    if subsep:
        return [nestedSplit(fragment, *subsep) for fragment in astring.split(sep)]
    return astring.split(sep)


if __name__ == '__main__':
    st = "a b\nc d"
    print st
    print nestedSplit(st, "\n", " ")
    print

    tetris = """\
    ....
    .##.
    .##.
    ....

    ####
    ####
    ..##
    ..##"""

    from textwrap import dedent
    tetris = dedent(tetris)
    print tetris
    print nestedSplit(tetris, "\n\n", "\n")
