# encdec.py
# File encryption/decryption using stream cipher
# FB - 201003066

import sys
import random

if len(sys.argv) != 5:
    print "Usage: encdec.py e/d longintkey [path]filename1 [path]filename2"
    sys.exit()

k = long(sys.argv[2]) # key
random.seed(k)

f1 = open( sys.argv[3], "rb")
bytearr = map (ord, f1.read () )
f2 = open( sys.argv[4], "wb" )

if sys.argv[1] == "e": # encryption

    for i in range(len(bytearr)):
        byt = (bytearr[i] + random.randint(0, 255)) % 256
        f2.write(chr(byt))


if sys.argv[1] == "d": # decryption

    for i in range(len(bytearr)):
        byt = ((bytearr[i] - random.randint(0, 255)) + 256 ) % 256
        f2.write(chr(byt))

f1.close()
f2.close()
