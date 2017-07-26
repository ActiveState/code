from struct import calcsize, pack, unpack

class ConcreteRecord(list):

    def __init__(self, fields, data=None, tu = False):
        self._fields = fields
        #self.tup = ()
        varspace = 0
        if data == None: return
        for f in fields:
            name,fmt,start,stop = f
            if fmt == 'z':
                strlen = data.find('\0', (start+varspace))-(start+varspace)
                val = data[(start+varspace):(start+varspace+strlen)]
                varspace += strlen + 1
            else:    
                val = unpack(fmt, data[(start+varspace):(stop+varspace)])
                if len(val) == 1: val=val[0]
            if tu == True:
                self.append(val,)
            else: 
                self.__dict__[name] = val

class RecordFactory:

    def __init__(self,record_fmt):
        self.fields = []
        pos = 0
        for field in record_fmt.split():
            if field[0] == "#": continue
            fmt,name = field.split('.')
            if fmt == 'z':
                size = 0
            else:
                size = calcsize(fmt)
            self.fields += [(name,fmt,pos,pos+size)]
            pos += size

    def build(self, data, tu  = False):
        return ConcreteRecord(self.fields, data, tu)

#### EXAMPLE ##################################################################

if __name__ == '__main__':

    myrf = RecordFactory("""
        z.test
        4B.ip
        z.zeroterm
        z.abc
        >H.port
        >I.session_id
    """)

    r = myrf.build("teast\x00\x00\x01\x02\x03" + "test\x00" + "abc\x00" + "\x00\x04" + "\xFE\xDC\xBA\x98")
    print "test:      ", r.test
    print "ip:        ", r.ip
    print "zeroterm:  ", r.zeroterm
    print "second string:  ", r.abc
    print "port:      ", r.port
    print "session_id:", r.session_id

    r = myrf.build("teast\x00\x00\x01\x02\x03" + "test\x00" + "abc\x00" + "\x00\x04" + "\xFE\xDC\xBA\x98",True)
    print r
