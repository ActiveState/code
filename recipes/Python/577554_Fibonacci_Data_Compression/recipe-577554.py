# Fibonacci Data Compression
# http://en.wikipedia.org/wiki/Fibonacci_coding
# (Max compressible file size: 2**32 bytes)
# FB - 201101274
import sys
import os

def encode_fib(n):
    # Return string with Fibonacci encoding for n (n >= 1).
    result = ""
    if n >= 1:
        a = 1
        b = 1
        c = a + b   # next Fibonacci number
        fibs = [b]  # list of Fibonacci numbers, starting with F(2), each <= n
        while n >= c:
            fibs.append(c)  # add next Fibonacci number to end of list
            a = b
            b = c
            c = a + b
        result = "1"  # extra "1" at end
        for fibnum in reversed(fibs):
            if n >= fibnum:
                n = n - fibnum
                result = "1" + result
            else:
                result = "0" + result
    return result

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
    print 'Usage: Fibonacci.py [e|d] [path]InputFileName [path]OutputFileName'
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

    # assign encoding bit strings to each byte value
    for b in range(len(tupleList)):
        tupleList[b] = (tupleList[b][0], tupleList[b][1], encode_fib(b + 1))
    # print 'The list of (frequency, byteValue, encodingBitStr) tuples:'
    # print tupleList
    # print

    # write the list of byte values as the compressed file header
    bitStream = '' # global
    fo = open(outputFile, 'wb')
    fo.write(chr(len(tupleList) - 1)) # first write the number of byte values
    for (freq, byteValue, encodingBitStr) in tupleList:
        # convert the byteValue into 8-bit and send to be written into file
        # bitStr = bin(byteValue)
        # bitStr = bitStr[2:] # remove 0b
        # bitStr = '0' * (8 - len(bitStr)) + bitStr # add 0's if needed for 8 bits
        # byteWriter(bitStr, fo)
        fo.write(chr(byteValue)) # this would do the same

    # write 32-bit (input file size)-1 value
    bitStr = bin(fileSize - 1)
    bitStr = bitStr[2:] # remove 0b
    bitStr = '0' * (32 - len(bitStr)) + bitStr # add 0's if needed for 32 bits
    byteWriter(bitStr, fo)

    # create a dictionary of byteValue : encodingBitStr pairs
    dic = dict([(tup[1], tup[2]) for tup in tupleList])
    # del tupleList
    # print 'The dictionary of byteValue : encodingBitStr pairs:'
    # print dic

    # write the encoded data
    for b in byteArr:
        byteWriter(dic[b], fo)

    byteWriter('0' * 8, fo) # to write the last remaining bits (if any)
    fo.close()

elif mode == 'd': # FILE DECODING
    bitPosition = 0 # global
    n = int(bitReader(8), 2) + 1 # first read the number of byte values
    # print 'Number of byte values:', n
    dic = dict()
    for i in range(n):
        # read the byteValue
        byteValue = int(bitReader(8), 2)
        encodingBitStr = encode_fib(i + 1)
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
            # if encodingBitStr in dic:
            if encodingBitStr.endswith('11'):
                byteValue = dic[encodingBitStr]
                fo.write(chr(byteValue))
                break
    fo.close()
