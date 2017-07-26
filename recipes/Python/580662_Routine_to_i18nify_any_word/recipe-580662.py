from __future__ import print_function
'''
Utility to "i18nify" any word given as argument.

You Heard It Here First (TM):
"i18nify" signifies making a numeronym of the given word, in the 
same manner that "i18n" is a numeronym for "internationalization" 
- because there are 18 letters between the starting "i" and the 
ending "n". Another example is "l10n" for "localization".
Also see a16z.

Author: Vasudev Ram
Copyright 2016 Vasudev Ram - https://vasudevram.github.io
'''

def i18nify(word):
    # If word is too short, don't bother, return as is.
    if len(word) < 4:
        return word
    # Return (the first letter) plus (the string form of the 
    # number of intervening letters) plus (the last letter).
    return word[0] + str(len(word) - 2) + word[-1]

def get_words():
    for words in [ \
        ['a', 'bc', 'def', 'ghij', 'klmno', 'pqrstu', 'vwxyz'], \
        ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', \
        'lazy', 'dog'], \
        ['all', 'that', 'glitters', 'is', 'not', 'gold'], \
        ['often', 'have', 'you', 'heard', 'that', 'told'], \
        ['jack', 'and', 'jill', 'went', 'up', 'the', 'hill', \
        'to', 'fetch', 'a', 'pail', 'of', 'water'],
    ]:
        yield words

def test_i18nify(words):
    print("\n")
    print(' '.join(words))
    print(' '.join([i18nify(word) for word in words]))

def main():
    for words in get_words():
        test_i18nify(words)
        print

if __name__ == "__main__":
    main()
