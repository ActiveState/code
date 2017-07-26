class LogicalLines:
    def __init__(self, fileobj, continued=None):
        # self.seq: the underlying line-sequence
        # self.phys_num: current index into self.seq (physical line number)
        # self.logi_num: current index into self (logical line number)
        import xreadlines
        try: self.seq = fileobj.xreadlines()
        except AttributeError: self.seq = xreadlines.xreadlines(fileobj)
        self.phys_num = 0
        self.logi_num = 0
        # allow for optional passing of continued-function
        if not callable(continued):
            def continued(line):
                if line.endswith('\\\n'): return 1,line[:-2]
                else: return 0, line
        self.continued = continued
    def __getitem__(self, index):
        if index != self.logi_num:
            raise TypeError, "Only sequential access supported"
        self.logi_num += 1
        result = []
        while 1:
            # Note: we must intercept IndexError, since we may not
            # be finished, even when the underlying sequence is --
            # we may have one or more lines in result to be returned
            try: line = self.seq[self.phys_num]
            except IndexError:
                if result: break
                else: raise
            self.phys_num += 1
            continues, line = self.continued(line)
            result.append(line)
            if not continues: break
        # return string result
        return ''.join(result)

# here's an example function, showing off usage:
def show_logicals(fileob,numlines=5):
    ll = LogicalLines(fileob)
    for l in ll:
        print "Log#%d, phys# %d: %s" % (
            ll.logi_num, ll.phys_num, repr(l))
        if ll.logi_num>numlines: break

if __name__=='__main__':
    from cStringIO import StringIO
    ff = StringIO(
"""prima \seconda \terza
quarta \quinta
sesta
settima \ottava
""")
    show_logicals( ff )

# a simpler approach, if the need is of a 1-off kind, might be:
# logical_line = []
# for physical_line in fileobj.xreadlines():
#     if physical_line.endswith('\\\n'):
#         logical_line.append(physical_line[:-2])
#     else:
#         logical_line = ''.join(logical_line) + physical_line
#         process_full_record(logical_line)
#         logical_line = []
# if logical_line: process_full_record(''.join(logical_line))
