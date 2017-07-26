import os
import sys

PRINT = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

def main():
    try:
        data = open(sys.argv[1], 'rb')
        for number in xrange(0, os.path.getsize(sys.argv[1]), 16):
            part = data.read(16)
            sys.stdout.write('%08X | %s | %s\n' % (number, hexit(part).ljust(47), clean(part)))
        data.close()
    except:
        sys.stdout.write('Usage: %s <filename>' % os.path.basename(sys.argv[0]))

def hexit(string):
    return ' '.join('%02X' % ord(c) for c in string)

def clean(string):
    return ''.join(c in PRINT and c or '.' for c in string)

if __name__ == '__main__':
    main()
