DEL = '/'
class PorReader(object):
    def __init__(self, file):
        if type(file) in (str, unicode): file = open(file)
        self.file = file
        self.pos = -1
        self.buffer = ""
    def consumeOne(self, skip=False):
        p = self.buffer.find(DEL, self.pos+1)
        output = ""
        while p == -1:
            if not skip: output += self.buffer[self.pos+1:]
            self.buffer = self.file.read(1024)
            self.pos = -1
            p = self.buffer.find(DEL, self.pos+1)
            if not self.buffer: break
        if not skip: output += self.buffer[self.pos+1:p]
        self.pos = p
        if not skip:
            output = output.replace("\r\n", "")
            return output
    def consume(self, n=1):
        return [self.consumeOne() for i in range(n)]
    def skip(self, n=1):
        for i in range(n):
            self.consumeOne(skip=True)

HEAD = 'SPSS for Microsoft Windows Release 15.04'

FLOAT, STR, INT = 0,1,2

class SPSSVariable(object):
    def __init__(self, name, label=None, numeric=True, decimals=0):
        self.name = name
        self.label = label
        self.numeric = numeric
        self.decimals = decimals
        self.valuelabels = None
        self.index = None
    def __str__(self):
        t = 'S'
        if self.numeric: t = 'I'
        if self.numeric and self.decimals: t = 'F'
        return "%s%s%s" % (self.name, (' "%s" ' % self.label if self.label else ''),t)

def splitstring(slen=None, s=None, reader=None):
    if slen is None:
        slen = reader.consume(2)
    if s is None: slen, s = slen
    if type(slen) == str: slen = readnum(slen)
    while slen > len(s):
        if reader:
            s += "/"+reader.consumeOne()
        else:
            raise Exception("!")
    keep = s[slen:]
    s = s[:slen]
    return s, keep

class SPSSFile(object):
    def __init__(self, file):
        self.variables = []
        self.vardict = {}
        self.data = []
        self.init(file)
    def addvar(self, var):
        var.index = len(self.variables)
        self.variables.append(var)
        self.vardict[var.name] = var
    def getvar(self, varname):
        return self.vardict[varname]
    def get(self, var, row):
        if type(var) in (str, unicode):
            var = self.vardict[var]
        return row[var.index]
    def init(self, file):
        r = PorReader(file)
        r.skip(5)
        h = r.consumeOne()
        if not h.startswith(HEAD): raise Exception("Cannot read .por")
        numvars = readnum(h[len(HEAD):])
        h = r.skip(1)
        keep = r.consumeOne()
        while True:
            action = keep[0]
            #print "ACTION: %s" % action
            if action == '7':
                data = r.consume(8)
                while data[-2][0] <> 'C': data += r.consume()
                decimals = readnum(data[4])
                numeric = keep[1:] == '0'
                name, dummy = splitstring(data[:2])
                labellen, label = data[-2:]
                label, keep = splitstring(labellen[1:], label, r)
                v = SPSSVariable(name, label, numeric, decimals)
                self.addvar(v)
                #print "ADDED VAR ", v, data, `keep`, labellen[1:]
            if action == 'D': # value labels
                numvars = readnum(keep[1:])
                varnames = []
                keep = r.consumeOne()
                for i in range(numvars):
                    name, keep = splitstring(keep, r.consumeOne(), reader=r)
                    varnames.append(name)
                numlabels = readnum(keep)
                keep = r.consumeOne()
                labels = {}
                numeric = self.getvar(varnames[0]).numeric
                for i in range(numlabels):
                    if numeric:
                        val = readnum(keep)
                        name, keep = splitstring(reader=r)
                    else:
                        val, keep = splitstring(keep, r.consumeOne(), reader=r)
                        name, keep = splitstring(keep, r.consumeOne(), reader=r)
                    labels[val] = name
                #print "VALUE LABELS", varnames, labels
                for varname in varnames:
                    self.getvar(varname).valuelabels = labels
            if action == 'F': # data
                keep = keep[1:]
                while True:
                    row = []
                    for var in self.variables:
                        if not keep: keep = r.consumeOne()
                        if keep.startswith("Z"):
                            return
                        if var.numeric:
                            if keep.startswith("*."):
                                row.append(None)
                                keep = keep[2:]
                            else:
                                try:
                                    row.append(readnum(keep))
                                except Exception, e:
                                    print row
                                    print "Exception on %s" % var
                                    raise e
                                keep = ""
                        else:
                            slen = keep
                            x, keep = splitstring(slen, r.consumeOne())
                            row.append(x)
                    self.data.append(tuple(row))
            if action == 'Z': # data
                print "Done!"
                return

def _codec(str_in, base_from=36, base_to=10):
    """
    Base36 Encoder/Decoder
    by Mike Crute (mcrute@gmail.com) on August 26, 2008
    This code has been placed in the public domain.
    """
    ASCII = { "0": 48, "9": 57, "A": 65, "Z": 90 }
    # There are 8 characters between 9 and A
    from_digits = [chr(x) for x in range(ASCII["0"], ASCII["9"] + 8 + base_from)
                            if (x >= ASCII["0"] and x <= ASCII["9"]) or
                               (x >= ASCII["A"] and x <= ASCII["Z"])][:base_from]
    to_digits = [chr(x) for x in range(ASCII["0"], ASCII["9"] + 8 + base_to)
                            if (x >= ASCII["0"] and x <= ASCII["9"]) or
                               (x >= ASCII["A"] and x <= ASCII["Z"])][:base_to]
    x = long(0)
    for digit in str(str_in).upper():
        x = x * len(from_digits) + from_digits.index(digit)
    result = ""
    # This is going to assemble our number in reverse order
    # so we'll have to fix it before we return it
    while x > 0:
        result += to_digits[x % len(to_digits)]
        x /= len(to_digits)
    return result[::-1]

def decode(s):
    while s.startswith("0"): s = s[1:]
    if not s: return 0
    try:
        return int(_codec(s, 30, 10))
    except ValueError, e:
        raise ValueError("Cannot decode %r: %s" % (s, e))


def readnum(s):
    neg = s.startswith("-")
    if neg: s = s[1:]
    if "+" in s:
        num, exp = map(decode, s.split("+"))
        result = 30**exp
    elif "-" in s:
        num, exp = map(decode, s.split("-"))
        result = 1. / (30**exp)
    else:
        if "." in s:
            i, d = s.split(".")
        else:
            i, d = s, None
        result = decode(i)
        if d:
            for j, digit in enumerate(d):
                result += decode(digit) / 30.**(j+1)
    return result * (-1 if neg else 1)



if __name__ == '__main__':
    import sys
    fn = sys.argv[1]
    f = SPSSFile(fn)
    print len(f.variables), len(f.data)
