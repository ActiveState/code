# Shannon-Fano Data Compression
# http://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding
# (Max compressible file size: 2**32 bytes)
# FB - 201012153
import sys
import os

def shannon_fano_encoder(iA, iB): # iA to iB : index interval
    global tupleList
    size = iB - iA + 1
    if size > 1:
        # Divide the list into 2 groups.
        # Top group will get 0, bottom 1 as the new encoding bit.
        mid = int(size / 2 + iA)
        for i in range(iA, iB + 1):
            tup = tupleList[i]
            if i < mid: # top group
                tupleList[i] = (tup[0], tup[1], tup[2] + '0')
            else: # bottom group
                tupleList[i] = (tup[0], tup[1], tup[2] + '1')
        # do recursive calls for both groups
        shannon_fano_encoder(iA, mid - 1)
        shannon_fano_encoder(mid, iB)

def byteWriter(bitStr, outputFile):
    global bitStream
    bitStream += bitStr
    while len(bitStream) > 8: # write byte(s) if there are more then 8 bits
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        outputFile.write(chr(int(byteStr, 2)))

def bitReader(n): # number of bits to read
    global byteArr
    global bitPosition
    bitStr = ''
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1 # prepare to read the next bit
    return bitStr

# MAIN
if len(sys.argv) != 4:
    print 'Usage: ShannonFano.py [e|d] [path]InputFileName [path]OutputFileName'
    sys.exit()
mode = sys.argv[1] # encoding/decoding
inputFile = sys.argv[2]
outputFile = sys.argv[3]

# read the whole input file into a byte array
fileSize = os.path.getsize(inputFile)
fi = open(inputFile, 'rb')
# byteArr = map(ord, fi.read(fileSize))
byteArr = bytearray(fi.read(fileSize))
fi.close()
fileSize = len(byteArr)
print 'File size in bytes:', fileSize
print

if mode == 'e': # FILE ENCODING
    # calculate the total number of each byte value in the file
    freqList = [0] * 256
    for b in byteArr:
        freqList[b] += 1

    # create a list of (frequency, byteValue, encodingBitStr) tuples
    tupleList = []
    for b in range(256):
        if freqList[b] > 0:
            tupleList.append((freqList[b], b, ''))

    # sort the list according to the frequencies descending
    tupleList = sorted(tupleList, key=lambda tup: tup[0], reverse = True)

    shannon_fano_encoder(0, len(tupleList) - 1)
    # print 'The list of (frequency, byteValue, encodingBitStr) tuples:'
    # print tupleList
    # print

    # create a dictionary of byteValue : encodingBitStr pairs
    dic = dict([(tup[1], tup[2]) for tup in tupleList])
    del tupleList # unneeded anymore
    # print 'The dictionary of byteValue : encodingBitStr pairs:'
    # print dic

    # write a list of (byteValue,3-bit(len(encodingBitStr)-1),encodingBitStr)
    # tuples as the compressed file header
    bitStream = ''
    fo = open(outputFile, 'wb')
    fo.write(chr(len(dic) - 1)) # first write the number of encoding tuples
    for (byteValue, encodingBitStr) in dic.iteritems():
        # convert the byteValue into 8-bit and send to be written into file
        bitStr = bin(byteValue)
        bitStr = bitStr[2:] # remove 0b
        bitStr = '0' * (8 - len(bitStr)) + bitStr # add 0's if needed for 8 bits
        byteWriter(bitStr, fo)
        # convert len(encodingBitStr) to 3-bit and send to be written into file
        bitStr = bin(len(encodingBitStr) - 1) # 0b0 to 0b111
        bitStr = bitStr[2:] # remove 0b
        bitStr = '0' * (3 - len(bitStr)) + bitStr # add 0's if needed for 3 bits
        byteWriter(bitStr, fo)
        # send encodingBitStr to be written into file
        byteWriter(encodingBitStr, fo)

    # write 32-bit (input file size)-1 value
    bitStr = bin(fileSize - 1)
    bitStr = bitStr[2:] # remove 0b
    bitStr = '0' * (32 - len(bitStr)) + bitStr # add 0's if needed for 32 bits
    byteWriter(bitStr, fo)

    # write the encoded data
    for b in byteArr:
        byteWriter(dic[b], fo)

    byteWriter('0' * 8, fo) # to write the last remaining bits (if any)
    fo.close()

elif mode == 'd': # FILE DECODING
    bitPosition = 0
    n = int(bitReader(8), 2) + 1 # first read the number of encoding tuples
    # print 'Number of encoding tuples:', n
    dic = dict()
    for i in range(n):
        # read the byteValue
        byteValue = int(bitReader(8), 2)
        # read 3-bit(len(encodingBitStr)-1) value
        m = int(bitReader(3), 2) + 1
        # read encodingBitStr
        encodingBitStr = bitReader(m)
        dic[encodingBitStr] = byteValue # add to the dictionary
    # print 'The dictionary of encodingBitStr : byteValue pairs:'
    # print dic
    # print

    # read 32-bit file size (number of encoded bytes) value
    numBytes = long(bitReader(32), 2) + 1
    print 'Number of bytes to decode:', numBytes
    
    # read the encoded data, decode it, write into the output file
    fo = open(outputFile, 'wb')
    for b in range(numBytes):
        # read bits until a decoding match is found
        encodingBitStr = ''
        while True:
            encodingBitStr += bitReader(1)
            if encodingBitStr in dic:
                byteValue = dic[encodingBitStr]
                fo.write(chr(byteValue))
                break
    fo.close()
