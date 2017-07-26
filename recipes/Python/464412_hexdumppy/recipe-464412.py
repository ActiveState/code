import os, sys

def main():
    try:
        engine(file(' '.join(sys.argv[1:]), 'rb', 0).read())
    except:
        print os.path.basename(sys.argv[0]), '<filename>'

def engine(string):
    if len(string) > 0:
        parts = divide(string, 16)
        for index in range(len(parts)):
            print ' | '.join([hex(index << 4)[2:].upper().zfill(8)[-8:], \
                              pad_right(convert_hex(parts[index]), 47), \
                              convert_print(parts[index])])

def divide(string, length):
    parts = list()
    for index in range(len(string[:-1]) / length + 1):
        parts.append(string[index*length:index*length+length])
    return parts

def pad_right(string, length, padding=' '):
    if len(string) < length:
        return string + padding[0] * (length - len(string))
    else:
        return string

def convert_hex(string):
    return ' '.join([hex(ord(character))[2:].upper().zfill(2) \
                     for character in string])

def convert_print(string):
    characters = str()
    rule = can_print()
    for character in string:
        if character in rule:
            characters += character
        else:
            characters += '.'
    return characters

def can_print():
    return ''.join([chr(byte) for byte in range(256) \
                    if len(repr(chr(byte))) == 3 or byte == ord('\\')])
                    
if __name__ == '__main__':
    main()
