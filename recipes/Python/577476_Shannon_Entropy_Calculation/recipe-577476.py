# Shannon Entropy of a string
# = minimum average number of bits per symbol
# required for encoding the string
#
# So the theoretical limit for data compression:
# Shannon Entropy of the string * string length
# FB - 201011291
import math
from sets import Set

st = 'aabcddddefffg' # input string
# st = '00010101011110' # Shannon entropy for this would be 1 bit/symbol

print 'Input string:'
print st
print
stList = list(st)
alphabet = list(Set(stList)) # list of symbols in the string
print 'Alphabet of symbols in the string:'
print alphabet
print
# calculate the frequency of each symbol in the string
freqList = []
for symbol in alphabet:
    ctr = 0
    for sym in stList:
        if sym == symbol:
            ctr += 1
    freqList.append(float(ctr) / len(stList))
print 'Frequencies of alphabet symbols:'
print freqList
print
# Shannon entropy
ent = 0.0
for freq in freqList:
    ent = ent + freq * math.log(freq, 2)
ent = -ent
print 'Shannon entropy:'
print ent
print 'Minimum number of bits required to encode each symbol:'
print int(math.ceil(ent))
