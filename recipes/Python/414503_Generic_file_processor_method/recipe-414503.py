def process_lines(fd, handler, cond=None):
    """
    Process all lines in fd

    if cond is not None, process only lines returning True for cond
    """

    if cond is not None:
        [ handler(line) for line in fd.readlines() if cond(line) ]
    else:
        [ handler(line) for line in fd.readlines() ]

if __name__ == '__main__':
    import sys

    fname = sys.argv[0]

    def line_printer(line):
        sys.stdout.write(line)

    # print all lines containing 'if'
    process_lines(file(fname), line_printer, lambda n: n.find('file') > -1)

    lst = []
    # read all lines to list
    process_lines(file(fname), lst.append)

    for line in lst:
        sys.stdout.write(line)
