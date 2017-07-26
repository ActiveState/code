# Hamming(7,4) Error Correction Code
# https://en.wikipedia.org/wiki/Hamming(7%2C4)
# FB - 20160723
import random

# the encoding matrix
G = ['1101', '1011', '1000', '0111', '0100', '0010', '0001']
# the parity-check matrix
H = ['1010101', '0110011', '0001111']
Ht = ['100', '010', '110', '001', '101', '011', '111']
# the decoding matrix
R = ['0010000', '0000100', '0000010', '0000001']

p = ''.join([random.choice('01') for k in range(4)])
print 'Input bit string: ' + p

x = ''.join([str(bin(int(i, 2) & int(p, 2)).count('1') % 2) for i in G])
print 'Encoded bit string to send: ' + x

# add 1 bit error
e = random.randint(0, 7)
# counted from left starting from 1
print 'Which bit got error during transmission (0: no error): ' + str(e)
if e > 0:
    x = list(x)
    x[e - 1] = str(1 - int(x[e - 1]))
    x = ''.join(x)
print 'Encoded bit string that got error during tranmission: ' + x 

z = ''.join([str(bin(int(j, 2) & int(x, 2)).count('1') % 2) for j in H])
if int(z, 2) > 0:
    e = int(Ht[int(z, 2) - 1], 2)
else:
    e = 0
print 'Which bit found to have error (0: no error): ' + str(e)

# correct the error
if e > 0:
    x = list(x)
    x[e - 1] = str(1 - int(x[e - 1]))
    x = ''.join(x)

p = ''.join([str(bin(int(k, 2) & int(x, 2)).count('1') % 2) for k in R])
print 'Corrected output bit string: ' + p 
