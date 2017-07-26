import re, sys
#import collections # For Python 2.5


def tabler(data, rjust=False):
    """tabler(data, rjust=False): given a string containing a textual table, splits it
    into a list of lists, according to the position of the most frequent word beginnings
    (or according to the most frequent word endings for tables aligned to the right).
    If the columns of the table are aligned to the right, then use rjust=True."""
    # Requires re module

    # RE to find the beginning of words
    tpatt = re.compile(r"(?:[ ]|^)[^ ]")

    # Remove empty lines
    lines = [line for line in data.splitlines() if line.strip()]

    if not lines:
        return [[]]

    # if the table is right justified, invert the lines
    if rjust:
        # to append spaces to the right, so when inverted they align vertically
        len_max = max(len(line) for line in lines)

        # Invert all the lines after appending the spaces
        lines = [line.ljust(len_max)[::-1] for line in lines]

    # Find the positions of all word beginnings
    # This finds:  treshs = [0, 11, 25, 35, 49, ...
    # 44544      ipod          apple     black         102
    # ^          ^             ^         ^             ^
    treshs = [ob.start() for li in lines for ob in tpatt.finditer(li)]

    # Find treshs frequences, old compatibility version
    freqs = {}
    for el in treshs:
        if el in freqs:
            freqs[el] += 1
        else:
            freqs[el] = 1

    # Find treshs frequences, alternative for Python V.2.5+
    # freqs = collections.defaultdict(int)
    # for el in treshs:
    #    freqs[el] += 1

    # Find a big enough frequence
    bigf = max(freqs.itervalues()) * 0.6

    # Find the most common column beginnings
    cols = sorted(k for k,v in freqs.iteritems() if v>bigf)

    def xpairs(alist):
        "xpairs(xrange(n)) ==> (0,1), (1,2), (2,3), ..., (n-2, n-1)"
        for i in xrange(len(alist)-1):
            yield alist[i:i+2]

    result = [[li[x:y].strip() for x,y in xpairs(cols+[None])] for li in lines]

    # if the table is right justified, invert the lines
    if rjust:
        result = [[el[::-1] for el in reversed(line)] for line in result]

    return result


if __name__ == '__main__': # Some demos
    from pprint import pprint

    data1 = """\
    44544      ipod          apple     black         102
    GFGFHHF-12 unknown thing bizar     brick mortar  tbc
    45fjk      do not know   + is less               biac
               disk          seagate   250GB         130
    5G_gff                   tbd       tbd
    gjgh88hgg  media record  a and b                 12
    hjj        foo           bar       hop           zip
    hg uy oi   hj uuu ii a   qqq ccc v ZZZ Ughj
    qdsd       zert                    nope          nope
    """
    print data1, "\n"
    pprint(tabler(data1))
    print

    data2 = """\
           44544           ipod      apple           black      102
      GFGFHHF-12  unknown thing      bizar    brick mortar      tbc
           45fjk    do not know  + is less                     biac
                           disk    seagate           250GB      130
          5G_gff                       tbd             tbd
       gjgh88hgg   media record    a and b                       12
             hjj            foo        bar             hop      zip
        hg uy oi    hj uuu ii a  qqq ccc v        ZZZ Ughj
            qdsd           zert                       nope     nope
    """
    print data2, "\n"
    pprint(tabler(data2, rjust=True))
    print


    data3 = """\
44544      ipod          apple     black         102
GFGFHHF-12 unknown thing bizar     brick mortar  tbc
    """
    print data3
    pprint(tabler(data3))
    print


    data4 = """
    """
    print data4
    pprint(tabler(data4))
    print


    data5 = """\
        A  B  C  D  E   F  G  H  I  K   L  M  N  P  Q   R  S  T  V  W   X  Y  Z  *
    A   4 -2  0 -2 -1  -2  0 -2 -1 -1  -1 -1 -2 -1 -1  -1  1  0  0 -3  -1 -2 -1 -4
    B  -2  6 -3  6  2  -3 -1 -1 -3 -1  -4 -3  1 -1  0  -2  0 -1 -3 -4  -1 -3  2 -4
    C   0 -3  9 -3 -4  -2 -3 -3 -1 -3  -1 -1 -3 -3 -3  -3 -1 -1 -1 -2  -1 -2 -4 -4
    D  -2  6 -3  6  2  -3 -1 -1 -3 -1  -4 -3  1 -1  0  -2  0 -1 -3 -4  -1 -3  2 -4
    E  -1  2 -4  2  5  -3 -2  0 -3  1  -3 -2  0 -1  2   0  0 -1 -2 -3  -1 -2  5 -4
    """
    print data5
    for line in tabler(data5, rjust=True):
        print " ".join(line)
