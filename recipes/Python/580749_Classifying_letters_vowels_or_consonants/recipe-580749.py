# classify_letters1.py

# Author: Vasudev Ram
# Copyright 2017 Vasudev Ram
# Web site: https://vasudevram.github.io
# Blog: https://jugad2.blogspot.com
# Product store: https://gumroad.com/vasudevram

# Classify input chars as vowels or consonants.
# Count frequencies of each vowel.
# Count total frequency of all consonants together.

import string

VOWELS = 'aeiou'

def classify_letters(input):
    vowel_freqs = { vowel: 0 for vowel in VOWELS }
    consonants = 0
    for c in input:
        if not (c in string.ascii_lowercase):
            continue
        if c in VOWELS:
            vowel_freqs[c] = vowel_freqs.get(c, 0) + 1
        else:
            consonants += 1
    return vowel_freqs, consonants

# Letter frequencies in s increase sequentially from 1 for both 
# vowels and consonants, separately.
s = ''.join(['a' * 1, 'b' * 1, 'c' * 2, 'd' * 3, 'e' * 2, 'f' * 4, \
    'g' * 5, 'h' * 6, 'i' * 3, 'j' * 7, 'k' * 8, 'l' * 9, 'm' * 10, \
    'n' * 11, 'o' * 4, 'p' * 12, 'q' * 13, 'r' * 14, 's' * 15, \
    't' * 16, 'u' * 5, 'w' * 17, 'y' * 18, 'z' * 19])

print "Classifying letters in string:", s
print '-' * 70
vowel_freqs, consonants = classify_letters(s)
print 'vowel freqs:', vowel_freqs
print 'consonants total freq:', consonants
print '-' * 70
print 'Checking results:'
assert len(s) == sum(vowel_freqs.values()) + consonants
print 'OK'
