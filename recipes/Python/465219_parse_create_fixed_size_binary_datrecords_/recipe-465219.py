from struct import calcsize, pack, unpack

class ConcreteRecord:

    def __init__(self, fields, data=None):
        self._fields = fields
        if data == None: return
        for f in fields:
            name,fmt,start,stop = f
            val = unpack(fmt, data[start:stop])
            if len(val) == 1: val=val[0]
            self.__dict__[name] = val

    def __str__(self):
        lst = []
        for f in self._fields:
            name,fmt,start,stop = f
            val = self.__dict__.get(name)
            if type(val) in (tuple,list):  # U
                lst += [pack(fmt,*val)]    # G
            else:                          # L
                lst += [pack(fmt,val)]     # Y
        return ''.join(lst)


class RecordFactory:

    def __init__(self,record_fmt):
        self.fields = []
        pos = 0
        for field in record_fmt.split():
            if field[0] == "#": continue
            fmt,name = field.split('.')
            size = calcsize(fmt)
            self.fields += [(name,fmt,pos,pos+size)]
            pos += size

    def build(self, data):
        return ConcreteRecord(self.fields, data)

#### EXAMPLE ##################################################################

myrf = RecordFactory("""
    4B.ip
    >H.port
    >I.session_id
""")

r = myrf.build("\x00\x01\x02\x03" + "\x00\x04" + "\xFE\xDC\xBA\x98")
print "ip:        ", r.ip
print "port:      ", r.port
print "session_id:", r.session_id

r.port       = 1029       # equals 0x0405
r.session_id = 101124105  # equals 0x06070809
import binascii
print "record_str:", binascii.hexlify(str(r))
