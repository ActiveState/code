import zlib, base64

def asciiCompress(data, level=9):
    """ compress data to printable ascii-code """

    code = zlib.compress(data,level)
    csum = zlib.crc32(code)
    code = base64.encodestring(code)
    return code, csum

def asciiDecompress(code):
    """ decompress result of asciiCompress """

    code = base64.decodestring(code)
    csum = zlib.crc32(code)
    data = zlib.decompress(code)
    return data, csum

if __name__ == "__main__":

    print
    print "TEST SELF COMPRESSION"

  
    text = file(__file__, "r").read()

    data = text+text+text

    print
    print "size uncompressed ............. :", len(data)

    code, csum1 = asciiCompress(data)

    print
    print "compressed data looks like this :", code[:35]
    print
    print "size compressed ............... :", len(code)
    print "compression effect ............ : %.1f %%" % (len(code)*100.0/len(data))
    print 

    datanew, csum2 = asciiDecompress(code)

    if datanew == data and csum1 == csum2:
        print "compress + decompress succeeded"
    else:
        print "compress + decompress failed"
    
