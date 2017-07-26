import string

#
# Relative letter frequencies for the french and english languages. 
# First item is letter 'A' frequency and so on.
#
ENGLISH = (0.0749, 0.0129, 0.0354, 0.0362, 0.1400, 0.0218, 0.0174, 0.0422, 0.0665, 0.0027, 0.0047, 0.0357, 
           0.0339, 0.0674, 0.0737, 0.0243, 0.0026, 0.0614, 0.0695, 0.0985, 0.0300, 0.0116, 0.0169, 0.0028, 
           0.0164, 0.0004)
           
FRENCH =  (0.0840, 0.0106, 0.0303, 0.0418, 0.1726, 0.0112, 0.0127, 0.0092, 0.0734, 0.0031, 0.0005, 0.0601,
           0.0296, 0.0713, 0.0526, 0.0301, 0.0099, 0.0655, 0.0808, 0.0707, 0.0574, 0.0132, 0.0004, 0.0045, 
           0.0030, 0.0012)          
FREQUENCIES = (ENGLISH, FRENCH)

# This program can be used to decipher Caesar encoding as produced by the
# function bellow
def cipher(s, key):
    r = ''
    ASC_A = ord('a')
    for c in s.lower():
        if 'a'<=c<='z':
             r += chr(ASC_A+(ord(c)-ASC_A+key)%26)
        else:
             r += c 
    return r

#compute letter frequencies delta
def delta(source, dest):
    N = 0.0
    for f1,f2 in zip(source, dest):
        N += abs(f1-f2)
    return N
    
# compute letter frequencies from a text
def frequency(s):
    D = dict([(c,0) for c in string.lowercase])
    N = 0.0
    for c in s:
        if 'a'<=c<='z':
            N += 1
            D[c] += 1
    L = D.items()
    L.sort()
    return [f/N for (l,f) in L]

# deciphering caesar code by letter frequencies analysis 
def decipher(s):
    deltamin = 1000
    bestrot = 0
    freq = frequency(s)
    for key in range(26):
        d = min([delta(freq[key:]+freq[:key], x) for x in FREQUENCIES])
        if d<deltamin:
            deltamin = d
            bestrot = key
    return cipher(s, -bestrot)
    


#
# Some tests
#

T1 = """
Python is an easy to learn, powerful programming language. It has 
efficient high-level data structures and a simple but effective approach 
to object-oriented programming. Python's elegant syntax and dynamic
typing, together with its interpreted nature, make it an ideal language 
for scripting and rapid application development in many areas on most platforms. 

Python tutorial
"""

T2 = """
He quoi ? charmante Elise, vous devenez melancolique, apres
les obligeantes assurances que vous avez eu la bonte de me donner de
votre foi ? Je vous vois soupirer, helas ! au milieu de ma joie. Est-ce
du regret, dites-moi, de m'avoir fait heureux, et vous repentez-vous de
cet engagement ou mes feux ont pu vous contraindre ?

Moliere (l'Avare)
"""

import random
for text in (T1,T2):
    key = random.randrange(26)
    X = cipher(text, key)
    print X
    print decipher(X)
