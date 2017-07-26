import random;
import sys;

nonword = "\n" # Since we split on whitespace, this can never be a word
w1 = nonword
w2 = nonword

# GENERATE TABLE
table = {}

for line in sys.stdin:
    for word in line.split():
        table.setdefault( (w1, w2), [] ).append(word)
        w1, w2 = w2, word

table.setdefault( (w1, w2), [] ).append(nonword) # Mark the end of the file

# GENERATE OUTPUT
w1 = nonword
w2 = nonword

maxwords = 10000

for i in xrange(maxwords):
    newword = random.choice(table[(w1, w2)])
    if newword == nonword: sys.exit()
    print newword;
    w1, w2 = w2, newword
