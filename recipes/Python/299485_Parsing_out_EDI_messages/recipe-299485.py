import array
import string
import sys

try:
    # If available use the psyco optimizing routines.  This will speed
    # up execution by 2x.
    import psyco.classes
    base_class = psyco.classes.psyobj
except ImportError:
    base_class = object

alphanums = string.letters + string.digits

class BadFile(Exception):
    """Raised when file corruption is detected."""

class Parser(base_class):
    """Parse out segments from the X12 raw data files.

    Raises the BadFile exception when data corruption is detected.

    Attributes:
        delimiters
            A string where
            [0] == segment separator
            [1] == element separator
            [2] == sub-element separator
            [3] == repetition separator (if ISA version >= 00405
    """
    def __init__(self, filename=None):
        self.delimiters = ''
        if filename:
            self.open_file(filename)

    def __iter__(self):
        """Return the iterator for use in a for loop"""
        return self

    def open_file(self, filename):
        self.fp = open(filename, 'r')
        self.in_isa = False

    def next(self):
        """return the next segment from the file or raise StopIteration

        Here we'll return the next segment, this will be a 'bare' segment
        without the segment terminator.

        We're using the array module.  Written in C this should be very
        efficient at adding and converting to a string.
        """
        seg = array.array('c')
        if not self.in_isa:
            #We're at the begining of a file or interchange so we need
            #to handle it specially.  We read in the first 105 bytes,
            #ignoring new lines.  After that we read in the segment
            #terminator.
            while len(seg) != 106:
                i = self.fp.read(1)
                if i == '\0': continue
                if i == '':
                    if len(seg) == 0:
                        # We have reached the end of the file normally.
                        raise StopIteration
                    else:
                        # We have reached the end of the file, this is an error
                        # since we are in the middle of an ISA loop.
                        raise BadFile('Unexpected EOF found')
                if len(seg) < 105:
                    # While we're still gathering the 'main' portion of the
                    # ISA, we ignore NULLs and newlines.
                    if i != '\n':
                        # We're still in the 'middle' of the ISA, we won't
                        # accept NULLs or line feeds.
                        try:
                            seg.append(i)
                        except TypeError:
                            # This should never occur in a valid file.
                            print 'Type error on appending "%s"' % i
                else:
                    # We're at the end of the ISA, we'll accept *any*
                    # character except the NULL as the segment terminator for
                    # now.  We'll check for validity next.
                    if i == '\n':
                        # Since we're breaking some lines at position
                        # 80 on a given line, we need to also check the
                        # first character after the line break to make
                        # sure that the newline is supposed to be the
                        # terminator.  If it is, we just backup to
                        # reset the file pointer and move on.
                        pos = self.fp.tell()
                        next_char = self.fp.read(1)
                        if next_char != 'G':
                            i = next_char
                        else:
                            self.fp.seek(pos)
                    try:
                        seg.append(i)
                    except TypeError:
                        print 'Type error on appending "%s"' % i

            self.version = seg[84:89].tostring()
            self.delimiters = seg[105] + seg[3] + seg[104]
            if self.version >= '00405':
                self.delimiters = seg[105] + seg[3] + seg[104] + seg[83]

            # Verify that the delimiters are valid.
            for delim in self.delimiters:
                if delim in alphanums:
                    raise BadFile('"%s" is not a valid delimiter' % delim)

            # Set the flag to process everything else as normal segments.
            self.in_isa = True

            # Pop off the segment terminator.
            seg.pop()
            return seg.tostring()
        else:
            #We're somewhere in the body of the X12 message.  We just
            #read until we find the segment terminator and return the
            #segment.  (We still ignore line feeds unless the line feed
            #is the segment terminator.
            if self.delimiters[0] == '\n':
                return self.fp.readline()[:-1]
            else:
                fp_read = self.fp.read
                while 1:
                    i = fp_read(1)
                    if i == '\0': continue
                    if i == self.delimiters[0]:
                        # End of segment found, exit the loop and return the
                        # segment.
                        segment = seg.tostring()
                        if segment.startswith('IEA'):
                            self.in_isa = False
                        return segment
                    elif i != '\n':
                        try:
                            seg.append(i)
                        except TypeError:
                            raise BadFile('Corrupt characters found in data or unexpected EOF')

if __name__ == '__main__':
    # Sample usage
    message = Parser('edifile.txt')
    for segment in message:
        elements = segment.split(message.delimiters[1])
        # Dispatch based on elements[0]...
