#
# enum.py
#
#	This file contains the enum class, which implements
#       C style enums for python
#

class EnumException(Exception): pass
class InvalidEnumVal(EnumException): pass
class InvalidEnum(EnumException): pass
class DuplicateEnum(EnumException): pass
class DuplicateEnumVal(EnumException): pass

class enum:
    def __init__(self, enumstr):
        self.lookup = { }
        self.reverseLookup = { }
        evalue = 0

        elist = enumstr.split(',')

        for e in elist:
            item = e.strip().split('=')

            ename = item[0].strip()
            if ename == '':
                continue

            if len(item) == 2:
                try:
                    evalue = int(item[1].strip(), 0)
                except ValueError:
                    raise InvalidEnumVal, 'Invalid value for: ' + ename
            elif len(item) != 1:
                raise InvalidEnum, "Invalid enum: " + e

            if self.lookup.has_key(ename):
                raise DuplicateEnum, "Duplicate enum name: " + ename
            if self.reverseLookup.has_key(evalue):
                raise DuplicateEnumVal,"Duplicate value %d for %s"%(evalue,ename)

            self.lookup[ename] = evalue
            self.reverseLookup[evalue] = ename
            evalue += 1

    def __getattr__(self, attr):
        return self.lookup[attr]

    def __len__(self):
        return len(self.lookup)

    def __repr__(self):
        s = ''
        values = self.lookup.values()
        values.sort()
        for e in values:
            s = s + '%s = %d\n' % (self.reverseLookup[e], e)
        return s

def main():
    str = """
JETTA,
RABBIT,
BEETLE,
THING=400,
PASSAT,
GOLF,
CABRIO=700,
EUROVAN,
"""
    v = enum(str)
    print v
    print 'PASSAT = %d' % v.PASSAT

    e1 = enum('TEST,,TEST2')
    print 'e1 len = %d' % len(e1)
    print e1

    try:
        e2 = enum('TEST,TEST1=jjj')
    except InvalidEnumVal, msg:
        print 'Invalid Enum Value Passed'
        print '    %s' % msg
    else:
        print 'Invalid Enum Value Failed'

    try:
        e2 = enum('TEST,TEST1=76=87=KJK')
    except InvalidEnum, msg:
        print 'Invalid Enum Passed'
        print '    %s' % msg
    else:
        print 'Invalid Enum Failed'

    try:
        e2 = enum('TEST,TEST')
    except DuplicateEnum, msg:
        print 'Duplicate Enum Passed'
        print '    %s' % msg
    else:
        print 'Duplicate Enum Failed'

    try:
        e2 = enum('TEST,TEST1=0')
    except DuplicateEnumVal, msg:
        print 'Duplicate Enum Val Passed'
        print '    %s' % msg
    else:
        print 'Duplicate Enum Val Failed'

if __name__ == "__main__":
    main()
