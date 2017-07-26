# copyright 2004 Michael D. Stenner <mstenner@ece.arizona.edu>
# license: LGPL

class xreverse:
    def __init__(self, file_object, buf_size=1024*8):
        self.fo = fo = file_object
        fo.seek(0, 2)        # go to the end of the file
        self.pos = fo.tell() # where we are 
        self.buffer = ''     # data buffer
        self.lbuf = []       # buffer for parsed lines
        self.done = 0        # we've read the last line
        self.jump = -1 * buf_size
        
        while 1:
            try:            fo.seek(self.jump, 1)
            except IOError: fo.seek(0)
            new_position = fo.tell()
            new = fo.read(self.pos - new_position)
            fo.seek(new_position)
            self.pos = new_position

            self.buffer = new + self.buffer
            if '\n' in new: break
            if self.pos == 0: return self.buffer

        nl = self.buffer.split('\n')
        nlb = [ i + '\n' for i in nl[1:-1] ]
        if not self.buffer[-1] == '\n': nlb.append(nl[-1])
        self.buffer = nl[0]
        self.lbuf = nlb

    def __iter__(self): return self

    def next(self):
        try:
            return self.lbuf.pop()
        except IndexError:
            fo = self.fo
            while 1:
                #get the next chunk of data
                try:            fo.seek(self.jump, 1)
                except IOError: fo.seek(0)
                new_position = fo.tell()
                new = fo.read(self.pos - new_position)
                fo.seek(new_position)
                self.pos = new_position

                nl = (new + self.buffer).split('\n')
                self.buffer = nl.pop(0)
                self.lbuf = [ i + '\n' for i in nl ]

                if self.lbuf: return self.lbuf.pop()
                elif self.pos == 0:
                    if self.done:
                        raise StopIteration
                    else:
                        self.done = 1
                        return self.buffer + '\n'

def dump(rtype, fn):
    import sys

    fo = file(fn)
    for line in rtype(fo):
        sys.stdout.write(line)
    fo.close()
    
def rereverse(rtype, fn):
    fo = file(fn)
    rev = [ line for line in xreverse(fo) ]
    rev.reverse()
    sys.stdout.writelines(rev)

def test_compare(rtype, fn):
    import sys, os

    t1 = os.times()

    fo = file(fn)
    for line in rtype(fo):
        pass
    fo.close()

    t2 = os.times()

    fo = file(fn)
    for line in fo.readlines():
        pass
    fo.close()

    t3 = os.times()

    for i in range(5):
        print t2[i] - t1[i], t3[i] - t2[i]
    


if __name__ == '__main__':
    import sys
    fn = sys.argv[1]
    #dump(xreverse, fn)
    #test_compare(xreverse, fn)
    rereverse(xreverse, fn)
