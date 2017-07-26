import binascii

def crc2hex(crc):
    res=''
    for i in range(4):
        t=crc & 0xFF
        crc >>= 8
        res='%02X%s' % (t, res)
    return res

if __name__=='__main__':
    test='hello world! and Python too ;)'
    crc=binascii.crc32(test)
    print 'CRC:', crc
    print 'CRC in hex:', crc2hex(crc)
