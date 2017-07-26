'''
Remove diacritical marks from strings containing characters from any
latin alphabets.

Tested on both Python 2.x and Python 3.x
'''
import unicodedata

def remove_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')

if __name__ == '__main__':
    import sys
    
    input = '\xc0 quelle \xe9cole va-tu?'

    if sys.hexversion >= 0x3000000:
        # On Python >= 3.0.0
        output = remove_diacritic(input).decode()
    else:
        # On Python < 3.0.0
        output = remove_diacritic(unicode(input, 'ISO-8859-1'))

    print(input)
    print(output)
    assert(output == 'A quelle ecole va-tu?')
