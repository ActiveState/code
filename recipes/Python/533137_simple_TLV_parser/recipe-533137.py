import struct

def tlvs(data):
    '''TLVs parser generator'''
    while data:
        try:
            type, length = struct.unpack('!HH', data[:4])
            value = struct.unpack('!%is'%length, data[4:4+length])[0]
        except: 
            print "Unproper TLV structure found: ", (data,)
            break
        yield type, value
        data = data[4+length:]

########### example ####################################

# building network ordered data as TLVs list
a = struct.pack('!HHI', 1,4,2)     # first tlv
a+= struct.pack('!HHI', 3,4,4)     # second tlv
a+= struct.pack('!HHII', 5,8,6,6)  # third tlv
a+= struct.pack('!HH', 2,3)        # unproper tlv

# using TLV parser generator
for type, data in tlvs(a):
    print type, (data,) #trick for print binary data

'''Produced output:
1 ('\x00\x00\x00\x02',)
3 ('\x00\x00\x00\x04',)
5 ('\x00\x00\x00\x06\x00\x00\x00\x06',)
Unproper TLV structure found:  ('\x00\x02\x00\x03',)
'''
