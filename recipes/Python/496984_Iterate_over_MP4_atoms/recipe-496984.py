import struct

FLAGS= CONTAINER, SKIPPER, TAGITEM, IGNORE, NOVERN, XTAGITEM= [2**_ for _ in xrange(6)]

# CONTAINER: datum contains other boxes
# SKIPPER: ignore first 4 bytes of datum
# TAGITEM: "official" tag item
# NOVERN: datum is 8 bytes (2 4-bytes BE integers)
# XTAGITEM: datum is a triplet (I believe) of "mean", "name", "data" items
CALLBACK= TAGITEM | XTAGITEM
FLAGS.append(CALLBACK)

TAGTYPES= (
    ('ftyp', 0),
    ('moov', CONTAINER),
    ('mdat', 0),
    ('udta', CONTAINER),
    ('meta', CONTAINER|SKIPPER),
    ('ilst', CONTAINER),
    ('\xa9ART', TAGITEM),
    ('\xa9nam', TAGITEM),
    ('\xa9too', TAGITEM),
    ('\xa9alb', TAGITEM),
    ('\xa9day', TAGITEM),
    ('\xa9gen', TAGITEM),
    ('\xa9wrt', TAGITEM),
    ('trkn', TAGITEM|NOVERN),
    ('\xa9cmt', TAGITEM),
    ('trak', CONTAINER),
    ('----', XTAGITEM),
    ('mdia', CONTAINER),
    ('minf', CONTAINER),
)

flagged= {}
for flag in FLAGS:
    flagged[flag]= frozenset(_[0] for _ in TAGTYPES if _[1] & flag)

def _xtra(s):
    "Convert '----' atom data into dictionaries"
    offset= 0
    result= {}
    while offset < len(s):
        atomsize= struct.unpack("!i", s[offset:offset+4])[0]
        atomtype= s[offset+4:offset+8]
        if atomtype == "data":
            result[atomtype]= s[offset+16:offset+atomsize]
        else:
            result[atomtype]= s[offset+12:offset+atomsize]
        offset+= atomsize
    return result

def _analyse(fp, offset0, offset1):
    "Walk the atom tree in a mp4 file"
    offset= offset0
    while offset < offset1:
        fp.seek(offset)
        atomsize= struct.unpack("!i", fp.read(4))[0]
        atomtype= fp.read(4)
        if atomtype in flagged[CONTAINER]:
            data= ''
            for reply in _analyse(fp, offset+(atomtype in flagged[SKIPPER] and 12 or 8),
                offset+atomsize):
                yield reply
        else:
            fp.seek(offset+8)
            if atomtype in flagged[TAGITEM]:
                data=fp.read(atomsize-8)[16:]
                if atomtype in flagged[NOVERN]:
                    data= struct.unpack("!ii", data)
            elif atomtype in flagged[XTAGITEM]:
                data= _xtra(fp.read(atomsize-8))
            else:
                data= fp.read(min(atomsize-8, 32))
        if not atomtype in flagged[IGNORE]: yield atomtype, atomsize, data
        offset+= atomsize

def mp4_atoms(pathname):
    fp= open(pathname, "rb")
    fp.seek(0,2)
    size=fp.tell()
    for atom in _analyse(fp, 0, size):
        yield atom
    fp.close()

class M4ATags(dict):
    "An example class reading .m4a tags"
    cvt= {
        'trkn': 'Track',
        '\xa9ART': 'Artist',
        '\xa9nam': 'Title',
        '\xa9alb': 'Album',
        '\xa9day': 'Year',
        '\xa9gen': 'Genre',
        '\xa9cmt': 'Comment',
        '\xa9wrt': 'Writer',
        '\xa9too': 'Tool',
    }
    def __init__(self, pathname=None):
        super(dict, self).__init__()
        if pathname is None: return
        for atomtype, atomsize, atomdata in mp4_atoms(pathname):
            self.atom2tag(atomtype, atomdata)

    def atom2tag(self, atomtype, atomdata):
        "Insert items using descriptive key instead of atomtype"
        if atomtype == "----":
            key= atomdata['name'].title()
            value= atomdata['data'].decode("utf-8")
        else:
            try: key= self.cvt[atomtype]
            except KeyError: return
            if atomtype == "trkn":
                value= atomdata[0]
            else:
                try: value= atomdata.decode("utf-8")
                except AttributeError:
                    print `atomtype`, `atomdata`
                    raise
        self[key]= value

if __name__=="__main__":
    import sys, pprint
    r= M4ATag(sys.argv[1]) # pathname of an .mp4/.m4a file as first argument
    pprint.pprint(r)
