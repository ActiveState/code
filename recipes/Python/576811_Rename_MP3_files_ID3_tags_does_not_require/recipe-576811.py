""" Read ID3 tags from a file.
    Ned Batchelder, http://nedbatchelder.com/code/modules/id3reader.html
    http://nedbatchelder.com/code/modules/id3reader.py

    * original code modified by ccpizza: added code to main method to rename
      files in current folder from ID3 tags,
      e.g. 'Track_01.mp3' >> '01 - Chan chan.mp3'
    * added safe console printing of unicode characters
    * added indexing for duplicate file names, i.e. '01 - Chan
chan.mp3[2]'
    * fixed indexing for duplicated ID3 tags
    * added -d option to create "artist\album" directories:
            e.g. 'Track_01.mp3' >> 'Compay Segundo\Mojito\01 - Chan chan.mp3'
    * added fallback to 'latin1' in case of non-unicode tag text
"""

__version__ = '1.53.20070415'    # History at the end of the file.

# ID3 specs: http://www.id3.org/develop.html

import struct, sys, zlib
import re

MP3=u'mp3'

# These are the text encodings, indexed by the first byte of a text value.
_encodings = ['iso8859-1', 'utf-16', 'utf-16be', 'utf-8']

# Simple pseudo-id's, mapped to their various representations.
# Use these ids with getValue, and you don't need to know what
# version of ID3 the file contains.
_simpleDataMapping = {
    'album':        ('TALB', 'TAL', 'v1album', 'TOAL'),
    'performer':    ('TPE1', 'TP1', 'v1performer', 'TOPE'),
    'title':        ('TIT2', 'TT2', 'v1title'),
    'track':        ('TRCK', 'TRK', 'v1track'),
    'year':         ('TYER', 'TYE', 'v1year'),
    'genre':        ('TCON', 'TCO', 'v1genre'),
    'comment':      ('COMM', 'COM', 'v1comment'),
}

# Provide booleans for older Pythons.
try:
    True, False
except NameError:
    True, False = 1==1, 1==0

# Tracing
_t = False
def _trace(msg):
    print msg

# Coverage
_c = False
_features = {}
def _coverage(feat):
    #if _t: _trace('feature '+feat)
    _features[feat] = _features.setdefault(feat, 0)+1

def _safestr(s):
    """ Get a good string for printing, that won't throw exceptions,
        no matter what's in it.
    """
    try:
        return unicode(s).encode(sys.getdefaultencoding())
    except UnicodeError:
        return '?: '+repr(s)

# Can I just say that I think the whole concept of genres is bogus,
# since they are so subjective?  And the idea of letting someone else pick
# one of these things and then have it affect the categorization of my music
# is extra bogus.  And the list itself is absurd. Polsk Punk?
_genres = [
    # 0-19
    'Blues', 'Classic Rock', 'Country', 'Dance', 'Disco', 'Funk', 'Grunge', 'Hip - Hop', 'Jazz', 'Metal',
    'New Age', 'Oldies', 'Other', 'Pop', 'R&B', 'Rap', 'Reggae', 'Rock', 'Techno', 'Industrial',
    # 20-39
    'Alternative', 'Ska', 'Death Metal', 'Pranks', 'Soundtrack', 'Euro - Techno', 'Ambient', 'Trip - Hop', 'Vocal', 'Jazz + Funk',
    'Fusion', 'Trance', 'Classical', 'Instrumental', 'Acid', 'House', 'Game', 'Sound Clip', 'Gospel', 'Noise',
    # 40-59
    'Alt Rock', 'Bass', 'Soul', 'Punk', 'Space', 'Meditative', 'Instrumental Pop', 'Instrumental Rock', 'Ethnic', 'Gothic',
    'Darkwave', 'Techno - Industrial', 'Electronic', 'Pop - Folk', 'Eurodance', 'Dream', 'Southern Rock', 'Comedy', 'Cult', 'Gangsta Rap',
    # 60-79
    'Top 40', 'Christian Rap', 'Pop / Funk', 'Jungle', 'Native American', 'Cabaret', 'New Wave', 'Psychedelic', 'Rave', 'Showtunes',
    'Trailer', 'Lo - Fi', 'Tribal', 'Acid Punk', 'Acid Jazz', 'Polka', 'Retro', 'Musical', 'Rock & Roll', 'Hard Rock',
    # 80-99
    'Folk', 'Folk / Rock', 'National Folk', 'Swing', 'Fast - Fusion', 'Bebob', 'Latin', 'Revival', 'Celtic', 'Bluegrass',
    'Avantgarde', 'Gothic Rock', 'Progressive Rock', 'Psychedelic Rock', 'Symphonic Rock', 'Slow Rock', 'Big Band', 'Chorus', 'Easy Listening', 'Acoustic',
    # 100-119
    'Humour', 'Speech', 'Chanson', 'Opera', 'Chamber Music', 'Sonata', 'Symphony', 'Booty Bass', 'Primus', 'Porn Groove',
    'Satire', 'Slow Jam', 'Club', 'Tango', 'Samba', 'Folklore', 'Ballad', 'Power Ballad', 'Rhythmic Soul', 'Freestyle',
    # 120-139
    'Duet', 'Punk Rock', 'Drum Solo', 'A Cappella', 'Euro - House', 'Dance Hall', 'Goa', 'Drum & Bass', 'Club - House', 'Hardcore',
    'Terror', 'Indie', 'BritPop', 'Negerpunk', 'Polsk Punk', 'Beat', 'Christian Gangsta Rap', 'Heavy Metal', 'Black Metal', 'Crossover',
    # 140-147
    'Contemporary Christian', 'Christian Rock', 'Merengue', 'Salsa', 'Thrash Metal', 'Anime', 'JPop', 'Synthpop'
    ]

class Id3Error(Exception):
    """ An exception caused by id3reader properly handling a bad ID3 tag.
    """
    pass

class _Header:
    """ Represent the ID3 header in a tag.
    """
    def __init__(self):
        self.majorVersion = 0
        self.revision = 0
        self.flags = 0
        self.size = 0
        self.bUnsynchronized = False
        self.bExperimental = False
        self.bFooter = False

    def __str__(self):
        return str(self.__dict__)

class _Frame:
    """ Represent an ID3 frame in a tag.
    """
    def __init__(self):
        self.id = ''
        self.size = 0
        self.flags = 0
        self.rawData = ''
        self.bTagAlterPreserve = False
        self.bFileAlterPreserve = False
        self.bReadOnly = False
        self.bCompressed = False
        self.bEncrypted = False
        self.bInGroup = False

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def _interpret(self):
        """ Examine self.rawData and create a self.value from it.
        """
        if len(self.rawData) == 0:
            # This is counter to the spec, but seems harmless enough.
            #if _c: _coverage('zero data')
            return

        if self.bCompressed:
            # Decompress the compressed data.
            self.rawData = zlib.decompress(self.rawData)

        if self.id[0] == 'T':
            # Text fields start with T
            encoding = ord(self.rawData[0])
            if 0 <= encoding < len(_encodings):
                #if _c: _coverage('encoding%d' % encoding)
                value = self.rawData[1:].decode(_encodings[encoding])
            else:
                #if _c: _coverage('bad encoding')
                value = self.rawData[1:]
            # Don't let trailing zero bytes fool you.
            if value:
                value = value.strip('\0')
            # The value can actually be a list.
            if '\0' in value:
                value = value.split('\0')
                #if _c: _coverage('textlist')
            self.value = value
        elif self.id[0] == 'W':
            # URL fields start with W
            self.value = self.rawData.strip('\0')
            if self.id == 'WXXX':
                self.value = self.value.split('\0')
        elif self.id == 'CDM':
            # ID3v2.2.1 Compressed Data Metaframe
            if self.rawData[0] == 'z':
                self.rawData = zlib.decompress(self.rawData[5:])
            else:
                #if _c: _coverage('badcdm!')
                raise Id3Error, 'Unknown CDM compression: %02x' % self.rawData[0]
            #@TODO: re-interpret the decompressed frame.

        elif self.id in _simpleDataMapping['comment']:
            # comment field

            # In limited testing a typical comment looks like
            # '\x00XXXID3v1 Comment\x00comment test' so in this
            # case we need to find the second \x00 to know where
            # where we start for a comment.  In case we only find
            # one \x00, lets just start at the beginning for the
            # value
            s = str(self.rawData)

            pos = 0
            count = 0
            while pos < len(s) and count < 2:
                if ord(s[pos]) == 0:
                    count = count + 1
                pos = pos + 1
            if count < 2:
                pos = 1

            if pos > 0 and pos < len(s):
                s = s[pos:]
                if ord(s[-1]) == 0:
                    s = s[:-1]

            self.value = s

class Reader:
    """ An ID3 reader.
        Create one on a file object, and then use getValue('TIT2') (for example)
        to pull values.
    """
    def __init__(self, file):
        """ Create a reader from a file or filename. """
        self.file = file
        self.header = None
        self.frames = {}
        self.allFrames = []
        self.bytesLeft = 0
        self.padbytes = ''

        bCloseFile = False
        # If self.file is a string of some sort, then open it to get a file.
        if isinstance(self.file, (type(''), type(u''))):
            self.file = open(self.file, 'rb')
            bCloseFile = True

        self._readId3()

        if bCloseFile:
            self.file.close()

    def _readBytes(self, num, desc=''):
        """ Read some bytes from the file.
            This method implements the "unsynchronization" scheme,
            where 0xFF bytes may have had 0x00 bytes stuffed after
            them.  These zero bytes have to be removed transparently.
        """
        #if _t: _trace("ask %d (%s)" % (num,desc))
        if num > self.bytesLeft:
            #if _c: _coverage('long!')
            raise Id3Error, 'Long read (%s): (%d > %d)' % (desc, num, self.bytesLeft)
        bytes = self.file.read(num)
        self.bytesLeft -= num

        if len(bytes) < num:
            #if _t: _trace("short read with %d left, %d total" % (self.bytesLeft, self.header.size))
            #if _c: _coverage('short!')
            raise Id3Error, 'Short read (%s): (%d < %d)' % (desc, len(bytes), num)

        if self.header.bUnsynchronized:
            nUnsync = 0
            i = 0
            while True:
                i = bytes.find('\xFF\x00', i)
                if i == -1:
                    break
                #if _t: _trace("unsync at %d" % (i+1))
                #if _c: _coverage('unsyncbyte')
                nUnsync += 1
                # This is a stuffed byte to remove
                bytes = bytes[:i+1] + bytes[i+2:]
                # Have to read one more byte from the file to adjust
                bytes += self.file.read(1)
                self.bytesLeft -= 1
                i += 1
            #if _t: _trace("unsync'ed %d" % (nUnsync))

        return bytes

    def _unreadBytes(self, num):
        self.file.seek(-num, 1)
        self.bytesLeft += num

    def _getSyncSafeInt(self, bytes):
        assert len(bytes) == 4
        if type(bytes) == type(''):
            bytes = [ ord(c) for c in bytes ]
        return (bytes[0] << 21) + (bytes[1] << 14) + (bytes[2] << 7) + bytes[3]

    def _getInteger(self, bytes):
        i = 0;
        if type(bytes) == type(''):
            bytes = [ ord(c) for c in bytes ]
        for b in bytes:
            i = i*256+b
        return i

    def _addV1Frame(self, id, rawData):
        if id == 'v1genre':
            assert len(rawData) == 1
            nGenre = ord(rawData)
            try:
                value = _genres[nGenre]
            except IndexError:
                value = "(%d)" % nGenre
        else:
            value = rawData.strip(' \t\r\n').split('\0')[0]
        if value:
            frame = _Frame()
            frame.id = id
            frame.rawData = rawData
            frame.value = value
            self.frames[id] = frame
            self.allFrames.append(frame)

    def _pass(self):
        """ Do nothing, for when we need to plug in a no-op function.
        """
        pass

    def _readId3(self):
        header = self.file.read(10)
        if len(header) < 10:
            return
        hstuff = struct.unpack('!3sBBBBBBB', header)
        if hstuff[0] != "ID3":
            # Doesn't look like an ID3v2 tag,
            # Try reading an ID3v1 tag.
            self._readId3v1()
            return

        self.header = _Header()
        self.header.majorVersion = hstuff[1]
        self.header.revision = hstuff[2]
        self.header.flags = hstuff[3]
        self.header.size = self._getSyncSafeInt(hstuff[4:8])

        self.bytesLeft = self.header.size

        self._readExtHeader = self._pass

        if self.header.majorVersion == 2:
            #if _c: _coverage('id3v2.2.%d' % self.header.revision)
            self._readFrame = self._readFrame_rev2
        elif self.header.majorVersion == 3:
            #if _c: _coverage('id3v2.3.%d' % self.header.revision)
            self._readFrame = self._readFrame_rev3
        elif self.header.majorVersion == 4:
            #if _c: _coverage('id3v2.4.%d' % self.header.revision)
            self._readFrame = self._readFrame_rev4
        else:
            #if _c: _coverage('badmajor!')
            raise Id3Error, "Unsupported major version: %d" % self.header.majorVersion

        # Interpret the flags
        self._interpretFlags()

        # Read any extended header
        self._readExtHeader()

        # Read the frames
        while self.bytesLeft > 0:
            frame = self._readFrame()
            if frame:
                frame._interpret()
                self.frames[frame.id] = frame
                self.allFrames.append(frame)
            else:
                #if _c: _coverage('padding')
                break

    def _interpretFlags(self):
        """ Interpret ID3v2.x flags.
        """
        if self.header.flags & 0x80:
            self.header.bUnsynchronized = True
            #if _c: _coverage('unsynctag')

        if self.header.majorVersion == 2:
            if self.header.flags & 0x40:
                #if _c: _coverage('compressed')
                # "Since no compression scheme has been decided yet,
                # the ID3 decoder (for now) should just ignore the entire
                # tag if the compression bit is set."
                self.header.bCompressed = True

        if self.header.majorVersion >= 3:
            if self.header.flags & 0x40:
                #if _c: _coverage('extheader')
                if self.header.majorVersion == 3:
                    self._readExtHeader = self._readExtHeader_rev3
                else:
                    self._readExtHeader = self._readExtHeader_rev4
            if self.header.flags & 0x20:
                #if _c: _coverage('experimental')
                self.header.bExperimental = True

        if self.header.majorVersion >= 4:
            if self.header.flags & 0x10:
                #if _c: _coverage('footer')
                self.header.bFooter = True

    def _readExtHeader_rev3(self):
        """ Read the ID3v2.3 extended header.
        """
        # We don't interpret this yet, just eat the bytes.
        size = self._getInteger(self._readBytes(4, 'rev3ehlen'))
        self._readBytes(size, 'rev3ehdata')

    def _readExtHeader_rev4(self):
        """ Read the ID3v2.4 extended header.
        """
        # We don't interpret this yet, just eat the bytes.
        size = self._getSyncSafeInt(self._readBytes(4, 'rev4ehlen'))
        self._readBytes(size-4, 'rev4ehdata')

    def _readId3v1(self):
        """ Read the ID3v1 tag.
            spec: http://www.id3.org/id3v1.html
        """
        self.file.seek(-128, 2)
        tag = self.file.read(128)
        if len(tag) != 128:
            return
        if tag[0:3] != 'TAG':
            return
        self.header = _Header()
        self.header.majorVersion = 1
        self.header.revision = 0

        self._addV1Frame('v1title', tag[3:33])
        self._addV1Frame('v1performer', tag[33:63])
        self._addV1Frame('v1album', tag[63:93])
        self._addV1Frame('v1year', tag[93:97])
        self._addV1Frame('v1comment', tag[97:127])
        self._addV1Frame('v1genre', tag[127])
        if tag[125] == '\0' and tag[126] != '\0':
            #if _c: _coverage('id3v1.1')
            self.header.revision = 1
            self._addV1Frame('v1track', str(ord(tag[126])))
        else:
            #if _c: _coverage('id3v1.0')
            pass
        return

    _validIdChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    def _isValidId(self, id):
        """ Determine if the id bytes make a valid ID3 id.
        """
        for c in id:
            if not c in self._validIdChars:
                #if _c: _coverage('bad id')
                return False
        #if _c: _coverage('id '+id)
        return True

    def _readFrame_rev2(self):
        """ Read a frame for ID3v2.2: three-byte ids and lengths.
            spec: http://www.id3.org/id3v2-00.txt
        """
        if self.bytesLeft < 6:
            return None
        id = self._readBytes(3, 'rev2id')
        if len(id) < 3 or not self._isValidId(id):
            self._unreadBytes(len(id))
            return None
        hstuff = struct.unpack('!BBB', self._readBytes(3, 'rev2len'))
        frame = _Frame()
        frame.id = id
        frame.size = self._getInteger(hstuff[0:3])
        frame.rawData = self._readBytes(frame.size, 'rev2data')
        return frame

    def _readFrame_rev3(self):
        """ Read a frame for ID3v2.3: four-byte ids and lengths.
        """
        if self.bytesLeft < 10:
            return None
        id = self._readBytes(4,'rev3id')
        if len(id) < 4 or not self._isValidId(id):
            self._unreadBytes(len(id))
            return None
        hstuff = struct.unpack('!BBBBh', self._readBytes(6,'rev3head'))
        frame = _Frame()
        frame.id = id
        frame.size = self._getInteger(hstuff[0:4])
        cbData = frame.size
        frame.flags = hstuff[4]
        #if _t: _trace('flags = %x' % frame.flags)
        frame.bTagAlterPreserve = (frame.flags & 0x8000 != 0)
        frame.bFileAlterPreserve = (frame.flags & 0x4000 != 0)
        frame.bReadOnly = (frame.flags & 0x2000 != 0)
        frame.bCompressed = (frame.flags & 0x0080 != 0)
        if frame.bCompressed:
            frame.decompressedSize = self._getInteger(self._readBytes(4, 'decompsize'))
            cbData -= 4
            #if _c: _coverage('compress')
        frame.bEncrypted = (frame.flags & 0x0040 != 0)
        if frame.bEncrypted:
            frame.encryptionMethod = self._readBytes(1, 'encrmethod')
            cbData -= 1
            #if _c: _coverage('encrypt')
        frame.bInGroup = (frame.flags & 0x0020 != 0)
        if frame.bInGroup:
            frame.groupid = self._readBytes(1, 'groupid')
            cbData -= 1
            #if _c: _coverage('groupid')

        frame.rawData = self._readBytes(cbData, 'rev3data')
        return frame

    def _readFrame_rev4(self):
        """ Read a frame for ID3v2.4: four-byte ids and lengths.
        """
        if self.bytesLeft < 10:
            return None
        id = self._readBytes(4,'rev4id')
        if len(id) < 4 or not self._isValidId(id):
            self._unreadBytes(len(id))
            return None
        hstuff = struct.unpack('!BBBBh', self._readBytes(6,'rev4head'))
        frame = _Frame()
        frame.id = id
        frame.size = self._getSyncSafeInt(hstuff[0:4])
        cbData = frame.size
        frame.flags = hstuff[4]
        frame.bTagAlterPreserve = (frame.flags & 0x4000 != 0)
        frame.bFileAlterPreserve = (frame.flags & 0x2000 != 0)
        frame.bReadOnly = (frame.flags & 0x1000 != 0)
        frame.bInGroup = (frame.flags & 0x0040 != 0)
        if frame.bInGroup:
            frame.groupid = self._readBytes(1, 'groupid')
            cbData -= 1
            #if _c: _coverage('groupid')

        frame.bCompressed = (frame.flags & 0x0008 != 0)
        if frame.bCompressed:
            #if _c: _coverage('compress')
            pass
        frame.bEncrypted = (frame.flags & 0x0004 != 0)
        if frame.bEncrypted:
            frame.encryptionMethod = self._readBytes(1, 'encrmethod')
            cbData -= 1
            #if _c: _coverage('encrypt')
        frame.bUnsynchronized = (frame.flags & 0x0002 != 0)
        if frame.bUnsynchronized:
            #if _c: _coverage('unsyncframe')
            pass
        if frame.flags & 0x0001:
            frame.datalen = self._getSyncSafeInt(self._readBytes(4, 'datalen'))
            cbData -= 4
            #if _c: _coverage('datalenindic')

        frame.rawData = self._readBytes(cbData, 'rev3data')

        return frame

    def getValue(self, id):
        """ Return the value for an ID3 tag id, or for a
            convenience label ('title', 'performer', ...),
            or return None if there is no such value.
        """
        if self.frames.has_key(id):
            if hasattr(self.frames[id], 'value'):
                return self.frames[id].value
        if _simpleDataMapping.has_key(id):
            for id2 in _simpleDataMapping[id]:
                v = self.getValue(id2)
                if v:
                    return v
        return None

    def getRawData(self, id):
        if self.frames.has_key(id):
            return self.frames[id].rawData
        return None

    def dump(self):
        import pprint
        print "Header:"
        print self.header
        print "Frames:"
        for fr in self.allFrames:
            if len(fr.rawData) > 30:
                fr.rawData = fr.rawData[:30]
        pprint.pprint(self.allFrames)
        for fr in self.allFrames:
            if hasattr(fr, 'value'):
                print '%s: %s' % (fr.id, _safestr(fr.value))
            else:
                print '%s= %s' % (fr.id, _safestr(fr.rawData))
        for label in _simpleDataMapping.keys():
            v = self.getValue(label)
            if v:
                print 'Label %s: %s' % (label, _safestr(v))

    def dumpCoverage(self):
        feats = _features.keys()
        feats.sort()
        for feat in feats:
            print "Feature %-12s: %d" % (feat, _features[feat])

# chars not allowed in filenames
illegal_chars = u'/\?=+<>:;"*|!@#$%^&*'

# http://code.activestate.com/recipes/65441/
def has_chars(raw, bad_chars):
    try:
        for c in bad_chars:
            if c in raw: return True
        return False
    except UnicodeDecodeError:
        return False

def replace_illegal_chars(raw):
    return ''.join([c in illegal_chars and '_' or c for c in raw])

def asci(*args):
    for arg in args:
        print arg.encode('us-ascii','xmlcharrefreplace'),
    print

def is_dupe(oldmp3, newmp3):
    #return bool(re.search(u'^'+orig+ r'(\[\d+\])?$', new))
    old=os.path.splitext(oldmp3)[0]
    new=os.path.splitext(newmp3)[0]
    return old.lower().startswith(new.lower())

def parse_index(f):
    rx = re.compile('(?P<name>.+)\[(?P<index>\d+?)\]$')
    mo = rx.search(f)
    if mo:
        return mo.group('name'), mo.group('index')
    else:
        return f, 0

if __name__ == '__main__':

    import os
    import optparse

    dodirs = False

    parser = optparse.OptionParser()
    parser.add_option('-l','--list',
                      action="store_true",
                      help='List ID3 tags only with no renaming',
                      default=False
                      )
    parser.add_option('-d', '--dirs',
                      action="store_true",
                      help="create album dirs",
                      default=False)
    (opts, args) = parser.parse_args(sys.argv[1:])

    if len(args):
        mp3dir = unicode(args[0])
    else:
        mp3dir = u'.'
    print
    if opts.list:
        print 'Listing ID3 tags in folder:', asci(os.path.abspath(mp3dir))
    else:
        print 'Renaming MP3 files in folder:', asci(os.path.abspath(mp3dir))
    print

    for fname in os.listdir(mp3dir):
        # uncomment if you want to process only files with .mp3 extension
        # if not fname.lower().endswith(MP3):
            # continue
        if os.path.isdir(fname):
            continue
        absfname = os.path.join(mp3dir, fname)
        try:
            id3r = Reader(absfname)
        except (Id3Error, UnicodeDecodeError), e:
            print e
            continue
        #id3r.dump()
        album = id3r.getValue('album')
        track = id3r.getValue('track')
        artist = id3r.getValue('performer')
        title = id3r.getValue('title')
        year = id3r.getValue('year')



        ### move files to dirs according to artist, album
        if opts.dirs and artist and album:
            dodirs = True
            mp3dir_full = os.path.join(mp3dir,
                                       replace_illegal_chars(artist),
                                       replace_illegal_chars(album))

            if not os.path.exists(mp3dir_full):
                try:
                        os.makedirs(mp3dir_full)
                except (IOError,WindowsError), e :
                    print
        else:
            mp3dir_full = mp3dir

        if not title:
            continue
        # replace tracks like '2/15' >> '02'
        if track and u'/' in track:
            track = track.split('/')[0]
        if track:
            track = track.zfill(2) # zero fill, i. e. '1' >> '01'

        if not track:
            track = ''

        if has_chars(title, illegal_chars):
            title = replace_illegal_chars(title)
        try:
            if isinstance(track, unicode) or isinstance(title, unicode):
               new_fname = track + u' - ' + title + u'.' + MP3
            ## try to fix non-unicode strings, only trying 'latin1'
            if isinstance(track, str) or isinstance(title, str):
               new_fname = track + ' - ' + title.decode('latin1') + '.' + MP3
        except UnicodeDecodeError:
            print 'Encoding error while processing title/track'
            continue
        new_dir = dodirs and mp3dir_full or mp3dir
        proposed_new_name = os.path.join(new_dir, new_fname)

        maxwidth = 35

        if opts.list:
            print '>',
        else:
            if not is_dupe(absfname, proposed_new_name):
                if os.path.exists(proposed_new_name):
                    for i in range(1,1000): # max 200 duplicates
                        parsed_name, idx = parse_index(os.path.splitext(proposed_new_name)[0])
                        new_fname = parsed_name + u'[' + unicode(idx+i) + u'].' + MP3
                        if not os.path.exists(new_fname):
                            break
                try:
                    os.rename(absfname, os.path.join(new_dir, new_fname))
                except Exception, e:
                    asci( 'Error: ', absfname.ljust(maxwidth), '>>>', proposed_new_name, str(e) )
            else:
                maxwidth -= len('Skipping...') + 1
                print 'Skipping...',

        asci((len(fname) > maxwidth and fname[:maxwidth-3] or fname).ljust(maxwidth), ' >>> ',  new_fname)
