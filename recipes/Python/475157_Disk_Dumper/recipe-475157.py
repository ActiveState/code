import os
import sys

SECTOR_SIZE = 512

def main():
    try:
        if len(sys.argv) != 4:
            raise Exception('Not Enough Arguments')
        else:
            program(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    except Exception, error:
        print os.path.basename(sys.argv[0]), '<drive> <first> <last>'
        print 'Note:', error

def program(drive, first, last):
    if first > last:
        first, last = last, first
    data = get_data(drive, first, last)
    sectors = partition(data, SECTOR_SIZE)
    show_hex(first, last, sectors)

def get_data(drive, first, last):
    if os.name == 'posix':
        drive = file('/dev/' + drive)
    elif os.name == 'nt':
        drive = file(r'\\.\%s:' % drive)
    else:
        raise Exception('Do Not Know How To Access Drives')
    return read_all(drive, first, last - first + 1)

def read_all(drive, start_sector, sectors_to_read):
    start = start_sector * SECTOR_SIZE
    end = sectors_to_read * SECTOR_SIZE
    all_data = ''
    while start > 0:
        temp = drive.read(start)
        if not temp:
            temp = drive.read(start)
            if not temp:
                raise Exception('Cannot Read First Sector')
        start -= len(temp)
    assert start == 0
    while end > 0:
        temp = drive.read(end)
        if not temp:
            temp = drive.read(end)
            if not temp:
                if not all_data:
                    raise Exception('Cannot Find Requested Data')
                return all_data
        all_data += temp
        end -= len(temp)
    assert end == 0
    return all_data

def partition(string, size):
    if len(string) % size:
        parts = len(string) / size + 1
    else:
        parts = len(string) / size
    return [string[index*size:index*size+size] for index in range(parts)]

def show_hex(first, last, sectors):
    print '=' * 77
    for index in range(len(sectors)):
        print 'SECTOR', index + first
        print '=' * 77
        engine(sectors[index], index + first)
        print '=' * 77

def engine(string, sector):
    parts = partition(string, 16)
    rule = printable()
    for index in range(len(parts)):
        print ' | '.join([hex(index + sector * 32)[2:].upper().zfill(7)[-7:] + '0', \
                          pad_right(convert_hex(parts[index]), 47), \
                          convert_print(parts[index], rule)])

def printable():
    return ''.join([chr(byte) for byte in range(256) \
                    if len(repr(chr(byte))) == 3 or byte == ord('\\')])

def pad_right(string, length, padding=' '):
        return string + padding[0] * (length - len(string))

def convert_hex(string):
    return ' '.join([hex(ord(character))[2:].upper().zfill(2) \
                     for character in string])

def convert_print(string, rule):
    return ''.join([character in rule and character \
                    or '.' for character in string])

if __name__ == '__main__':
    main()
