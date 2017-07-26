# !/bin/sh
#
# Bin2Hex2Dec.sh
#
# A DEMO shell script to show how to display the contents of a binary file onto the screen and convert any
# single one of those hexadecimal contents to decimal, retrieve the decimal string and use it in a simple
# addition of the retrieved decimal string with a fixed number to give a result. The idea was to be able to
# get a byte value from say an external source and use it inside a bash script, in this case a value stored
# on the HDD.
#
# This DEMO was only designed for a Macbook Pro 13 inch, OSX 10.7.5 using the default, (BASH?), Terminal.
# It also works on Debian 6.0.x, PCLinuxOS 2009, Ubuntu, Fedora 17 using various Shells/Terminals.
#
# To run use the usual method for launching an _executable_ from its /directory/drawer/folder:-
#
# xxxxx$ ./Bin2Hex2Dec.sh<CR>
#
# And away you go...
#
# This script will need to be made executable using the command "chmod" and will save and load files to YOUR
# default /directory/drawer/folder. The files saved to the HDD will be named:-
# BinaryString.dat
# BinaryString.txt
# The output should look like this:-
#
#######################################
#
# $VER: Bin2Hex2Dec.sh_Version_0.00.10_Public_Domain_B.Walker_G0LCU.
#
# Generate and save a binary file, display a hexadecimal dump of that file,
# select a single byte from this binary file, display as a decimal number in
# string format then add this string number to another number...
#
# Offset.                  Hexadecimal dump.                      ASCII dump.
# 00000000  00 07 0a 0d 7f 28 43 29  32 30 31 32 2c 20 42 2e  |.....(C)2012, B.|
# 00000010  57 61 6c 6b 65 72 2c 20  47 30 4c 43 55 2e 80 ff  |Walker, G0LCU...|
# 00000020
#
# Now obtain the _byte_, from offset 0 in this DEMO, the first byte in the
# file, (0x00), and convert to a decimal string from the hexadecimal byte...
#
# Decimal value in string format = 0...
#
# Now ADD a number 7 to the decoded decimal string. 0 + 7 = 7...
#
# (Now edit the script and change the _variable_ ~subscript~ to another value.)
#
# Barrys-MacBook-Pro:~ barrywalker$ 
#
#######################################
#
# $VER: Bin2Hex2Dec.sh_Version_0.00.10_Public_Domain_B.Walker_G0LCU.
# This is Public Domain and you may do with it as you please. Ignore the (C) inside the code...

# Set up a simple user screen/window...
clear
printf "\n\$VER: Bin2Hex2Dec.sh_Version_0.00.10_Public_Domain_B.Walker_G0LCU.\n"
printf "\nGenerate and save a binary file, display a hexadecimal dump of that file,\n"
printf "select a single byte from this binary file, display as a decimal number in\n"
printf "string format then add this string number to another number...\n\n"

# NOTE:- Double back slashes required to ensure binary is saved rather than the string.
# The inverted commas ARE required!
binstr="\\x00\\x07\\x0A\\x0D\\x7F(C)2012, B.Walker, G0LCU.\\x80\\xFF"

# NOTE:- Inverted commas around "$binstr" and save 32 byte long string as BinaryString.dat into your default drawer.
printf "$binstr" > BinaryString.dat

# Do a text hexadecimal dump to the screen only of the 32 byte string...
printf "Offset.                  Hexadecimal dump.                      ASCII dump.\n"
hexdump -C BinaryString.dat

# Just an offset is needed for a single byte with a "subsript" offset inside the range of 0 to 31 for this 32 byte dump.
# The first byte is chosen for this DEMO. Just change this value to anything between 0 and 31 inclusive.
subscript=0

# Now select this single byte and save the value as a decimal string.
hexdump -n1 -s$subscript -v -e '1/1 "%u"' BinaryString.dat > BinaryString.txt

# Allow time for grabbed decimal byte value string to settle.
sleep 1

# The "subscript" offset is set at the first byte in the string, value zero, (0)...
printf "\nNow obtain the _byte_, from offset 0 in this DEMO, the first byte in the\n"
printf "file, (0x00), and convert to a decimal string from the hexadecimal byte...\n\n"

# Now retrieve the decimal byte string for further use from the file "BinaryString.txt".
read somedata < "BinaryString.txt"

# Now manipulate the retrieved string by adding a number to it...
printf "Decimal value in string format = $somedata...\n\n"
printf "Now ADD a number 7 to the decoded decimal string. $somedata + 7 = "$(($somedata+7))"...\n\n"
printf "(Now edit the script and change the _variable_ ~subscript~ to another value.)\n\n"

# Bin2Hex2Dec.sh DEMO end.
# Enjoy finding simple solutions to often very difficult problems... ;o)
