TEXT_CHARS =("0000000111101100" # 0x0X   
	     "0000000000010000" # 0x1X    This table give for each characters
      	     "1111111111111111" # 0x2X    the kind of ASCII text file it can
	     "1111111111111111" # 0x3X    belong to.
	     "1111111111111111" # 0x4X 
	     "1111111111111111" # 0x5X 
	     "1111111111111111" # 0x6X    0  never appears in text
	     "1111111111111110" # 0x7X    1  appears in plain ASCII text
	     "3333313333333333" # 0x8X    2  appears in ISO-8859 text
	     "3333333333333333" # 0x9X    3  appears in non-ISO extended-
	     "2222222222222222" # 0xaX       ASCII (Mac, IBM PC)
	     "2222222222222222" # 0xbX 
	     "2222222222222222" # 0xcX 
	     "2222222222222222" # 0xdX    This table is copyrighted,
	     "2222222222222222" # 0xeX    see the discussion part.
	     "2222222222222222")# 0xfX 

PLAIN_ASCII = ''.join([chr(i) for i in range(256) if TEXT_CHARS[i]=='1'])

def ascii_encoding(s):
    """ return 0 if the text s is not an ascii text, 1 if the text
        is a plain ASCII text, 2 if the text is ISO-8859, 3 if the file 
        is an non ISO extended text file"""
    s = s.translate(TEXT_CHARS, PLAIN_ASCII)
    for i in "032":
        if i in s:
            return int(i)
    return 1

#
#  some samples
#
print ascii_encoding("Hello wolrd")
print ascii_encoding("Sébastien Keim")
print ascii_encoding("AZZ\x12BB")
