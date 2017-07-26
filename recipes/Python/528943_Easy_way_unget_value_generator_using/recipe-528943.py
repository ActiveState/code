from __future__ import with_statement

def readFile(filename):
    with open(filename, 'r') as f:
        for l in f:
            if not l.isspace() and not l.startswith('#'):
                r = yield l.rstrip()
                if r:
                    # The first yield is needed because 'send' also
                    # yields a value
                    yield None
                    yield l.rstrip()


def processFirstPart(lines):
    l = lines.next()
    while l.isdigit():
        print l
        l = lines.next()
    # The last line was not a digit, but that doesn't mean we can
    # simply discard it.
    lines.send(1)

def processSecondPart(lines):
    l = lines.next()
    assert l == 'START'
    try:
        while True:
            print l
            l = lines.next()
    except StopIteration:
        pass

lines = readFile('example.in')

processFirstPart(lines)
print 'Going to the second part.'
processSecondPart(lines)
