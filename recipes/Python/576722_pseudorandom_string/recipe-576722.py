import os, math
from base64 import b64encode

randStr = lambda n: b64encode(os.urandom(int(math.ceil(0.75*n))),'-_')[:n]
