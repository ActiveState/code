import sys
import hashlib

def main():
    try:
        file = open(sys.argv[1], 'rb')
        md5 = hashlib.md5()
        buffer = file.read(2 ** 20)
        while buffer:
            md5.update(buffer)
            buffer = file.read(2 ** 20)
        file.close()
        print(md5.hexdigest())
    except:
        import os
        print('Usage: {0} <filename>'.format(os.path.basename(sys.argv[0])))

if __name__ == '__main__':
    main()
