"""Credits: 
Raymond Hettinger suggested using itertools
Chris Perkins suggested using itertools.imap
Bengt Richter suggested the name any_true
many others gave useful input on c.l.py
I did cut and paste ;)"""

import os,itertools
def anyTrue(pred,seq):
    "Returns True if a True predicate is found, False
    otherwise. Quits as soon as the first True is found"
    return True in itertools.imap(pred,seq)

# example: print image files in the current directory 
the=anyTrue # for readability
for filename in os.listdir('.'):
    if the(filename.endswith,('.jpg','.jpeg','.gif')):
       print filename
