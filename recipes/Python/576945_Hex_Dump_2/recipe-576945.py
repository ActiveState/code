import sys, os

def main():
    try:
        file = open(sys.argv[1], 'rb')
        for line in range(0, os.path.getsize(sys.argv[1]), 16):
            data = file.read(16)
            print('{:08X} | {:47} | {}'.format(line, hex(data), str(data)))
        file.close()
    except:
        print('Usage: {} <filename>'.format(os.path.basename(sys.argv[0])))

hex = lambda data: ' '.join('{:02X}'.format(i) for i in data)

str = lambda data: ''.join(31 < i < 127 and chr(i) or '.' for i in data)

if __name__ == '__main__':
    main()
