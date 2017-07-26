from ctypes import windll, create_string_buffer

# stdin handle is -10
# stdout handle is -11
# stderr handle is -12

h = windll.kernel32.GetStdHandle(-12)
csbi = create_string_buffer(22)
res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

if res:
    import struct
    (bufx, bufy, curx, cury, wattr,
     left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    sizex = right - left + 1
    sizey = bottom - top + 1
else:
    sizex, sizey = 80, 25 # can't determine actual size - return default values

print sizex, sizey
