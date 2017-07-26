# Initialisation
# 32 first bits of generator polynomial for CRC64
# the 32 lower bits are assumed to be zero

POLY64REVh = 0xd8000000L
CRCTableh = [0] * 256
CRCTablel = [0] * 256
isInitialized = False

def CRC64(aString):
    global isInitialized
    crcl = 0
    crch = 0
    if (isInitialized is not True):
        isInitialized = True
        for i in xrange(256): 
            partl = i
            parth = 0L
            for j in xrange(8):
                rflag = partl & 1L                
                partl >>= 1L               
                if (parth & 1):
                    partl |= (1L << 31L)
                parth >>= 1L
                if rflag:
	                parth ^= POLY64REVh
            CRCTableh[i] = parth;
            CRCTablel[i] = partl;

    for item in aString:
        shr = 0L
        shr = (crch & 0xFF) << 24
        temp1h = crch >> 8L
        temp1l = (crcl >> 8L) | shr                        
        tableindex = (crcl ^ ord(item)) & 0xFF
        
        crch = temp1h ^ CRCTableh[tableindex]
        crcl = temp1l ^ CRCTablel[tableindex]
    return (crch, crcl)

def CRC64digest(aString):
    return "%08X%08X" % (CRC64(aString))

if __name__ == '__main__':
    assert CRC64("IHATEMATH") == (3822890454, 2600578513)
    assert CRC64digest("IHATEMATH") == "E3DCADD69B01ADD1"
    print 'CRC64: dumb test successful'
      
