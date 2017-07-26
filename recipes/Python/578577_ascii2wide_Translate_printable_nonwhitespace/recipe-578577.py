from string import printable, whitespace

def ascii2wide(ascii):
    wide = []
    for letter in ascii:
        if letter in whitespace or letter not in printable:
            wide.append(letter)
        else:
            wide.append(chr(ord(letter) + 0xFEE0))

    return ''.join(wide)
