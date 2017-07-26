#################
# Morse Code 1.py
#################

import sys
import time
import winsound

DOT = 0.1
DASH = DOT * 3

BETWEEN_PARTS = DOT * 1
BETWEEN_LETTERS = DOT * 3
BETWEEN_WORDS = DOT * 7

CODE = {'A': [DOT, DASH],
        'B': [DASH, DOT, DOT, DOT],
        'C': [DASH, DOT, DASH, DOT],
        'D': [DASH, DOT, DOT],
        'E': [DOT],
        'F': [DOT, DOT, DASH, DOT],
        'G': [DASH, DASH, DOT],
        'H': [DOT, DOT, DOT, DOT],
        'I': [DOT, DOT],
        'J': [DOT, DASH, DASH, DASH],
        'K': [DASH, DOT, DASH],
        'L': [DOT, DASH, DOT, DOT],
        'M': [DASH, DASH],
        'N': [DASH, DOT],
        'O': [DASH, DASH, DASH],
        'P': [DOT, DASH, DASH, DOT],
        'Q': [DASH, DASH, DOT, DASH],
        'R': [DOT, DASH, DOT],
        'S': [DOT, DOT, DOT],
        'T': [DASH],
        'U': [DOT, DOT, DASH],
        'V': [DOT, DOT, DOT, DASH],
        'W': [DOT, DASH, DASH],
        'X': [DASH, DOT, DOT, DASH],
        'Y': [DASH, DOT, DASH, DASH],
        'Z': [DASH, DASH, DOT, DOT],
        '1': [DOT, DASH, DASH, DASH, DASH],
        '2': [DOT, DOT, DASH, DASH, DASH],
        '3': [DOT, DOT, DOT, DASH, DASH],
        '4': [DOT, DOT, DOT, DOT, DASH],
        '5': [DOT, DOT, DOT, DOT, DOT],
        '6': [DASH, DOT, DOT, DOT, DOT],
        '7': [DASH, DASH, DOT, DOT, DOT],
        '8': [DASH, DASH, DASH, DOT, DOT],
        '9': [DASH, DASH, DASH, DASH, DOT],
        '0': [DASH, DASH, DASH, DASH, DASH],
        '.': [DOT, DASH, DOT, DASH, DOT, DASH],
        ',': [DASH, DASH, DOT, DOT, DASH, DASH],
        '?': [DOT, DOT, DASH, DASH, DOT, DOT],
        '/': [DASH, DOT, DOT, DASH, DOT],
        '@': [DOT, DASH, DASH, DOT, DASH, DOT]}

def translate(string):
    for character in string.upper():
        if CODE.has_key(character):
            for interval in CODE[character]:
                winsound.Beep(440, int(interval * 1000))
                time.sleep(BETWEEN_PARTS)
            time.sleep(BETWEEN_LETTERS - BETWEEN_PARTS)
            sys.stdout.write(character)
        else:
            time.sleep(BETWEEN_WORDS - BETWEEN_LETTERS)
            sys.stdout.write(' ')

def test():
    line = sys.stdin.readline()
    while line:
        translate(line)
        sys.stdout.write('\n')
        line = sys.stdin.readline()

if __name__ == '__main__':
    test()

#################
# Morse Code 2.py
#################

from sys import *
from time import *
from winsound import *

################################################################################

FQC = 880
DOT = 0.1

################################################################################

DAH = DOT * 3
SEP = DOT * 7

CODE = {' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'}

################################################################################

def main():
    s = stdin.readline()
    while s:
        translate(s)
        s = stdin.readline()
    
def translate(s):
    s = ''.join(c for c in s.upper() if c in CODE)
    for i, c in enumerate(s):
        if c == ' ':
            sleep(SEP)
        else:
            for d in CODE[c][:-1]:
                Beep(FQC, int((DOT if d == '.' else DAH) * 1000))
                sleep(DOT)
            Beep(FQC, int((DOT if CODE[c][-1] == '.' else DAH) * 1000))
            if i + 1 != len(s) and s[i + 1] != ' ':
                sleep(DAH)

################################################################################
                
if __name__ == '__main__':
    main()
