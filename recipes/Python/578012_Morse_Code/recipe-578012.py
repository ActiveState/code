from time import sleep
from winsound import Beep

################################################################################

# CONSTANTS DEFINED BY USER

FQC = 800
DOT = 0.1

################################################################################

# CONSTANTS DEFINED BY STANDARD

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

# MAIN PROGRAM FUNCTIONS

def main():
    "Loop while getting, compiling, and executing given text."
    data = input()
    while data:
        _execute(_compile(data))
        data = input()

def _compile(data):
    "Format string as a series of timing codes for execution."
    code = []
    for word in ''.join(key for key in data.upper() if key in CODE).split():
        for character in word:
            for symbol in CODE[character]:
                code.extend(((DAH, DOT)[symbol == '.'], DOT))
            code[-1] = DAH
        code[-1] = SEP
    return tuple(code)

def _execute(code, ops=(lambda t: Beep(FQC, round(t * 1000)), sleep)):
    "Run timing codes with 'Beep' and 'sleep' by their order."
    for i, time in enumerate(code):
        ops[i & 1](time)

################################################################################

# STANDARD CONDITIONAL EXECUTION

if __name__ == '__main__':
    main()
