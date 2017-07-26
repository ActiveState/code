'''
Read and write data to a Lego Mindstorm NXT brick using serial bluetooth
connection.  You'll need to modify __init__ for unix style serial port 
identification in order to use this on Linux.

Blue enables raw byte transfer
TypeBlue utilizes NXT mailbox number for type identification.

Usage:
1. Enable a bluetooth serial port to accept connection requests from NXT.
2. Find and connect computer from NXT bluetooth menu.  Note serial port
   number; store in comport_num.

3. From python try this code, note the try finally and make sure the connection
   is established so that you are not waiting all the time for timeouts!  It is
   a real pain getting the comport back from a dropped connection.
   
import blueNXT
try:
    b = blueNXT.TypeBlue(comport_num)
    b.put('Hello NXT!')
    b.putall(False, True, 1, 'two')
    b.get()
finally:
    b.close()

4.  Write an interface to remote control your robots and share!
'''
__author__ = 'Justin Shaw'
import sys
import serial
import struct
import time

class Blue:
    '''
    A bluetooth connection to a Lego NXT brick
    '''
    huh = struct.pack('h', 2432) # don't really know what this is

    def __init__(self, comport=9, filename=None, mode='r', timeout=10):
        '''
        comport - integer com number for serial port
        filename and mode are for debug
        '''
        if filename is None:
            self.s = serial.Serial('COM%d' % comport, timeout=timeout)
        else:
            self.s = open(filename, mode)

    def get(self):
        '''
        Return payload, payload
        
        Get next message from NXT, return un-molested payload i.e. bytes.
        Use get_int() for integers and get_bool() for booleans
        '''
        sz = self.s.read(2)
        payload = None
        box = None
        if len(sz) == 2:
            sz = struct.unpack('h', sz)[0]
            # print 'sz', sz
            if 0 < sz < 1000:
                msg = self.s.read(sz)
                # print 'msg', msg
                dat = msg[:4]
                # for c in dat:
                #     print ord(c)
                # print struct.unpack('h', msg[:2])
                box = ord(dat[2]) + 1
                payload = msg[4:-1]
        return payload, box

    def put(self, payload, box=1):
        '''
        Send a raw message to NXT
        payload -- bytes to send
        box -- 1 to 10, which mail box on NXT to place message in
        '''
        # sz    msg----> 0
        # 0123456789 ... n
        payload += chr(0)
        pl_sz = len(payload)
        sz = pl_sz + 4
        header = struct.pack('h2sbb', sz, self.huh, box - 1, pl_sz)
        out = struct.pack('6s%ds' % pl_sz, header, payload)
        # print 'out', out
        dat = out[2:6]
        # for c in dat:
        #     print ord(c)
        # print
        # self.s.write('\x11\x00\x80\t\x00\r<0123456789>\x00')
        self.s.write(out)

    def __del__(self):
        try:
            self.close()
        except:
            pass
    def close(self):
        self.s.close()
        
class TypeBlue(Blue):
    '''
    Use mailbox number for type information:
    1 -- string
    2 -- int
    3 -- bool

    else -- string
    '''
    
    def get(self):
        '''
        Get a message off port.  Determine type from box number:
        1 -- string
        2 -- int
        3 -- bool
        '''
        msg, box = Blue.get(self)
        if box == 2:
            out = struct.unpack('i', msg)[0]
        elif box == 3:
            out = not not(ord(msg))
        else:
            out = msg
        return out
    
    def put(self, val):
        '''
        Put a message on port.  Use box to indicate type:
        1 -- string
        2 -- int
        3 -- bool
        '''
        if type(val) == type(''):
            msg = val
            box = 1
        elif type(val) == type(0):
            msg = struct.pack('i', val)
            box = 2
        elif type(val) == type(False):
            msg = struct.pack('b', not not val)
            box = 3
        return Blue.put(self, msg, box)

    def putall(self, *vals):
        '''
        Send several values to NXT
        '''
        for v in vals:
            self.put(v)

def Blue__test__():
    '''
    Test that the formats are consistant by reading and writing
    to a file.  No real bluetooth required.
    '''
    # read
    b = Blue(filename='text.dat')
    target = '<0123456789>'
    for i in range(10):
        msg, box = b.get()
        assert msg == target, '%s != %s' % (msg, target)

    # write
    b = Blue(filename='junk', mode='wb')
    b.put(target, 2)
    b = Blue(filename='junk')
    got, box = b.get()
    assert box == 2
    assert got == target, '%s != %s' % (got, target)
    b = Blue(filename='num.dat')

    # type
    b = TypeBlue(filename='junk', mode='wb')
    b.put(target)
    b.put(1)
    b.put(False)
    b = TypeBlue(filename='junk')
    got = b.get()
    assert got == target
    got = b.get()
    assert got == 1
    got = b.get()
    assert got == False
    
def tblue():
    '''
    Real bluetooth test.
    '''
    try:
        b = TypeBlue('COM10')
        for i in range(20):
            ##  only uncomment these if you have the NXT code sending data!
            # print b.get()
            # print b.get()
            # print b.get()
            # b.put(42)
            # b.put(False)
            b.put('HERE % d' % i)
            b.put(i)
            if i < 10:
                b.put(False)
            else:
                b.put(True)
            time.sleep(.25)
    finally:
        del b
# tblue()
# Blue__test__()
