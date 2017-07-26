# !/bin/sh
#
# BFM.sh
# A very simple DEMO Binary File Manipulation shell code issued entirely as Public Domain.
#
# Apologies for any typos...
#
# This is a DEMO to show how to generate binaryfiles in the shell.
# I need this facility for a kids project I am doing. It will be posted onto here in
# the not too distant future...
#
# To run, ensure the script is executable and from a terminal type:-
#
# *****$ /absolute/path/to/BFM.sh<CR>
#
# And away you go...
#
# Many thanks to MartyBartFast of the Linux Format forums for reminding me of the backticks... ;o)
#
# Written so that kids and newbies can understand what is going on...
#
# $VER: BFM.sh_Version_0.00.10_Public_Domain_2013_B.walker_G0LCU.
#
# Enjoy finding simple solutions to often very difficult problems...

# These two files WILL be generated inside YOUR default /directory/drawer/folder/...
# Zero them as a starter JUST for this DEMO...
> SomeBinaryFile.dat
> MyBinaryFile.dat

# This loop is to give a usable 256 byte binary file only from 0x00 to 0xFF continuous...
clear
for character in {0..255}
do
	# Note:- The backticks and the four escape characters are required...
	char=`printf '\\\\x'"%02x" $character`
	printf "$char" >> SomeBinaryfile.dat
done

# Do a hexadecimal dump to prove the file is binary and 256 bytes in size...
printf "\nOffset.                    Hexadecimal Dump.                    ASCII Dump.\n"
hexdump -C SomeBinaryFile.dat

# Now this EXAMPLE loop is the working loop. The three variables set the "start", (_offset_), of where you want
# your file to start, the "jump" between each _sample_ and the last_byte_limit to where you want to finish...
# IMPORTANT!!! There is NO error detection or correction in the code as it is a DEMO so don't come back and
# say that you can crash it, e.g. setting the "last_byte_limit" to -1 for example...
# Also although I am using a "for" loop for this DEMO you could select a single byte manually and code accordingly...
#
# The _variables_ for this DEMO. The jump is set to every seventh byte for this DEMO.
start_offset=4
jump=7
last_byte_limit=200

# _hexdump_ is used to select the byte(s) according to this DEMO "for" loop...
for subscript in $( seq $start_offset $jump $last_byte_limit )
do
	number=`hexdump -n1 -s$subscript -v -e '1/1 "%u"' SomeBinaryFile.dat`
	char=`printf '\\\\x'"%02x" $number`
	printf "$char" >> MyBinaryFile.dat
done
# Now display it...
printf "\nOffset.                    Hexadecimal Dump.                    ASCII Dump.\n"
hexdump -C MyBinaryFile.dat

# A terminal window dump of what should occur...
#
# Offset.                    Hexadecimal Dump.                    ASCII Dump.
# 00000000  00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f  |................|
# 00000010  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f  |................|
# 00000020  20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f  | !"#$%&'()*+,-./|
# 00000030  30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f  |0123456789:;<=>?|
# 00000040  40 41 42 43 44 45 46 47  48 49 4a 4b 4c 4d 4e 4f  |@ABCDEFGHIJKLMNO|
# 00000050  50 51 52 53 54 55 56 57  58 59 5a 5b 5c 5d 5e 5f  |PQRSTUVWXYZ[\]^_|
# 00000060  60 61 62 63 64 65 66 67  68 69 6a 6b 6c 6d 6e 6f  |`abcdefghijklmno|
# 00000070  70 71 72 73 74 75 76 77  78 79 7a 7b 7c 7d 7e 7f  |pqrstuvwxyz{|}~.|
# 00000080  80 81 82 83 84 85 86 87  88 89 8a 8b 8c 8d 8e 8f  |................|
# 00000090  90 91 92 93 94 95 96 97  98 99 9a 9b 9c 9d 9e 9f  |................|
# 000000a0  a0 a1 a2 a3 a4 a5 a6 a7  a8 a9 aa ab ac ad ae af  |................|
# 000000b0  b0 b1 b2 b3 b4 b5 b6 b7  b8 b9 ba bb bc bd be bf  |................|
# 000000c0  c0 c1 c2 c3 c4 c5 c6 c7  c8 c9 ca cb cc cd ce cf  |................|
# 000000d0  d0 d1 d2 d3 d4 d5 d6 d7  d8 d9 da db dc dd de df  |................|
# 000000e0  e0 e1 e2 e3 e4 e5 e6 e7  e8 e9 ea eb ec ed ee ef  |................|
# 000000f0  f0 f1 f2 f3 f4 f5 f6 f7  f8 f9 fa fb fc fd fe ff  |................|
# 00000100
#
# Offset.                    Hexadecimal Dump.                    ASCII Dump.
# 00000000  04 0b 12 19 20 27 2e 35  3c 43 4a 51 58 5f 66 6d  |.... '.5<CJQX_fm|
# 00000010  74 7b 82 89 90 97 9e a5  ac b3 ba c1 c8           |t{...........|
# 0000001d
# Barrys-MacBook-Pro:~ barrywalker$ 
#
# BFM.sh DEMO end...
# Enjoy finding simple solutions to often very difficult problems...
