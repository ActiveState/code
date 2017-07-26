from struct import unpack
from datetime import datetime

class FLVReader(dict):
    """
    Reads metadata from FLV files
    """

    # Tag types
    AUDIO = 8
    VIDEO = 9
    META = 18
    UNDEFINED = 0

    def __init__(self, filename):
        """
        Pass the filename of an flv file and it will return a dictionary of meta
        data.
        """
        # Lock on to the file
        self.file = open('x.flv', 'rb')
        self.signature = self.file.read(3)
        assert self.signature == 'FLV', 'Not an flv file'
        self.version = self.readbyte()
        self.typeFlags = self.readbyte()
        self.dataOffset = self.readint()
        extraDataLen = self.dataOffset - self.file.tell()
        self.extraData = self.file.read(extraDataLen)
        self.readtag()

    def readtag(self):
        unknown = self.readint()
        tagType = self.readbyte()
        dataSize = self.read24bit()
        timeStamp = self.read24bit()
        unknown = self.readint()
        if tagType == self.AUDIO:
            print "Can't handle audio tags yet"
        elif tagType == self.VIDEO:
            print "Can't handle video tags yet"
        elif tagType == self.META:
            endpos = self.file.tell() + dataSize
            event = self.readAMFData()
            metaData = self.readAMFData()
            # We got the meta data.
            # Our job is done.
            # We are complete
            self.update(metaData)
        elif tagType == self.UNDEFINED:
            print "Can't handle undefined tags yet"

    def readint(self):
      data = self.file.read(4)
      return unpack('>I', data)[0]

    def readshort(self):
      data = self.file.read(2)
      return unpack('>H', data)[0]

    def readbyte(self):
      data = self.file.read(1)
      return unpack('B', data)[0]

    def read24bit(self):
      b1, b2, b3 = unpack('3B', self.file.read(3))
      return (b1 << 16) + (b2 << 8) + b3

    def readAMFData(self, dataType=None):
        if dataType is None:
            dataType = self.readbyte()
        funcs = {
            0: self.readAMFDouble,
            1: self.readAMFBoolean,
            2: self.readAMFString,
            3: self.readAMFObject,
            8: self.readAMFMixedArray,
           10: self.readAMFArray,
           11: self.readAMFDate
        }
        func = funcs[dataType]
        if callable(func):
            return func()

    def readAMFDouble(self):
        return unpack('>d', self.file.read(8))[0]

    def readAMFBoolean(self):
        return self.readbyte() == 1

    def readAMFString(self):
        size = self.readshort()
        return self.file.read(size)

    def readAMFObject(self):
        data = self.readAMFMixedArray()
        result = object()
        result.__dict__.update(data)
        return result

    def readAMFMixedArray(self):
        size = self.readint()
        result = {}
        for i in range(size):
            key = self.readAMFString()
            dataType = self.readbyte()
            if not key and dataType == 9:
                break
            result[key] = self.readAMFData(dataType)
        return result

    def readAMFArray(self):
        size = self.readint()
        result = []
        for i in range(size):
            result.append(self.readAMFData)
        return result

    def readAMFDate(self):
        return datetime.fromtimestamp(self.readAMFDouble())
        

if __name__ == '__main__':
    import sys
    from pprint import pprint
    if len(sys.argv) == 1:
        print 'Usage: %s filename [filename]...' % sys.argv[0]
        print 'Where filename is a .flv file'
        print 'eg. %s myfile.flv' % sys.argv[0]
    for fn in sys.argv[1:]:
        x = FLVReader(fn)
        pprint(x)
