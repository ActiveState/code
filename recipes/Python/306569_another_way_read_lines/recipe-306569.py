import sys
if sys.platform[:3] == 'win':
    # use this under MS Windows or if you're going to read
    # MS Windows-formatted text files on other OSes using
    # the "univeral" option to open()
    def find_offsets(infile):
        offsets = []
        while 1:
            offset = infile.tell()
            if not infile.readline():
                break
            offsets.append(offset)
        return offsets
else:
    # Assumes the file uses a newline convention which is
    # one byte long.
    def find_offsets(infile):
        offsets = []
        offset = 0
        for line in infile:
            offsets.append(offset)
            offset += len(line)
        return offsets

def iter_backwards(infile):
    # make sure it's seekable and at the start
    infile.seek(0)
    offsets = find_offsets(infile)
    for offset in offsets[::-1]:
        infile.seek(offset)
        yield infile.readline()

# An example of how to use the new iterator

for line in iter_backwards(open("spam.py")):
    print repr(line)
