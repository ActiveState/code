import os
import sys

def main():
    try:
        table = [0] * 256
        data = open(sys.argv[1], 'rb')
        buff = data.read(2 ** 20)
        while buff:
            for c in buff:
                table[ord(c)] += 1
            buff = data.read(2 ** 20)
        data.close()
        sys.stdout.write(
            '\n'.join('%02X = %d' % (i, c) for i, c in enumerate(table) if c))
    except:
        sys.stdout.write('Usage: %s <filename>' % os.path.basename(sys.argv[0]))

if __name__ == '__main__':
    main()
