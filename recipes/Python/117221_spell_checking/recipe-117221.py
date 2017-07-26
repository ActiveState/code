#
# ispell interface tested with ispell 3.2.03

import popen2


class ispell:
    def __init__(self):
        self._f = popen2.Popen3("ispell")
        self._f.fromchild.readline() #skip the credit line
    def __call__(self, word):
        self._f.tochild.write(word+'\n')
        self._f.tochild.flush()
        s = self._f.fromchild.readline()
        self._f.fromchild.readline() #skip the blank line
        if s[:8]=="word: ok":
            return None
        else:
            return (s[17:-1]).split(', ')


f = ispell()
print f('hello')
print f('stinge')
