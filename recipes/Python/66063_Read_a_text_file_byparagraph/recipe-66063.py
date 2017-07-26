class Paragraphs:
    def __init__(self, fileobj, separator=None):
        # self.seq: the underlying line-sequence
        # self.line_num: current index into self.seq (line number)
        # self.para_num: current index into self (paragraph number)
        import xreadlines
        try: self.seq = fileobj.xreadlines()
        except AttributeError: self.seq = xreadlines.xreadlines(fileobj)
        self.line_num = 0
        self.para_num = 0
        # allow for optional passing of separator-function
        if separator is None:
            def separator(line): return line == '\n'
        elif not callable(separator):
            raise TypeError, "separator argument must be callable"
        self.separator = separator
    def __getitem__(self, index):
        if index != self.para_num:
            raise TypeError, "Only sequential access supported"
        self.para_num += 1
        # start where we left off, and skip 0+ separator lines
        i = self.line_num
        while 1:
            # note: if this raises IndexError, it's OK to propagate
            # it, since we're also a finished-sequence in this case
            line = self.seq[i]
            i += 1
            if not self.separator(line): break
        # accumulate 1+ non-blank lines into list result
        result = [line]
        while 1:
            # here we must intercept IndexError, since we're not
            # finished, even when the underlying sequence is --
            # we have one or more lines in result to be returned
            try: line = self.seq[i]
            except IndexError: break
            i += 1
            if self.separator(line): break
            result.append(line)
        # update self state, return string result
        self.line_num = i
        return ''.join(result)

# here's an example function, showing off usage:
def show_paragraphs(filename,numpars=5):
    pp = Paragraphs(open(filename))
    for p in pp:
        print "Par#%d, line# %d: %s" % (
            pp.para_num, pp.line_num, repr(p))
        if pp.para_num>numpars: break
