# slicing is great, of course, but it only does one field at a time:
afield = theline[3:8]

# if you want to think in terms of field-length, struct.unpack may 
# sometimes be handier:
import struct

# get a 5-byte string, skip 3, then get 2 8-byte strings, then all the rest:
baseformat = "5s 3x 8s 8s"
numremain = len(theline)-struct.calcsize(baseformat)
format = "%s %ds" % (baseformat, numremain)
leading, s1, s2, trailing = struct.unpack(format, theline)

# of course, the computation of the last field's length is best
# encapsulated in a function:
def fields(baseformat, theline, lastfield=None):
    numremain = len(theline)-struct.calcsize(baseformat)
    format = "%s %d%s" % (baseformat, numremain, lastfield and "s" or "x")
    return struct.unpack(format, theline)
# note that caching/memoizing on (baseformat, len(theline), lastfield) may
# well be useful here if this is called in a loop -- an easy speedup

# split at five byte boundaries:
numfives, therest = divmod(len(theline), 5)
form5 = "%s %dx" % ("5s "*numfives, therest)
fivers = struct.unpack(form5, theline)

# again, this is no doubt best encapsulated:
def split_by(theline, n, lastfield=None):
    numblocks, therest = divmod(len(theline), n)
    baseblock = "%d%s"%(n,lastfield and "s" or "x")
    format = "%s %dx"%(baseblock*numblocks, therest)

# chopping a string into individual characters is of course easier:
chars = list(theline)

# if you prefer to think of your data as being cut up at specific columns,
# then slicing and list comprehensions may be handier:
cuts = [8,14,20,26,30]
pieces = [ theline[i:j] for i, j in zip([0]+cuts, cuts+[sys.maxint]) ]

# once more, encapsulation is advisable:
def split_at(theline, cuts, lastfield=None):
    pieces = [ theline[i:j] for i, j in zip([0]+cuts, cuts) ]
    if lastfield:
        pieces.append(theline(cuts[-1]:))
    return pieces
