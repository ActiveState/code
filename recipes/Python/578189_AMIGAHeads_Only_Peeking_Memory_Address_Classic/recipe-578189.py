# AMIGA_Peek_Mem.py
#
# DEMO code to show how to peek/read a single BYTE from any address for the
# Classic AMIGA A1200(HD), E-UAE and WinUAE. Although the code only does BYTE
# depth it is easily possible to add, WORD length, (I've already done so).
# (Soon there will be a demo to poke/write to a memory or HW address inside the
# Classic AMIGA too.)
#
# Originally written for a standard AMIGA A1200 using Python 1.4.x to 2.0.1.
# $VER: AMIGA_Peek_Mem.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.
#
# Doing the 256 byte dump in this DEMO is slow but this function was not
# originally designed for that facility but to quickly view the byte contents
# of a single memory address. To work correctly this MUST be run from a "tool"
# icon so that any AMIGA return code Failat reports are directed to the system
# "stderr" rather than the default Python window...
#
# Now issued as Public Domain. You may do with it as you please...
#
# =============================================================================
#
# ; The assembly code for this Python script, peek.asm...
# ; Assembled using a68k and linked using blink, both are on AMINET.
#        lea.l	$00F80000,a5    ;Set address to the default start of ROM.
#        move.b	(a5),d0         ;Move byte contents of the address into register d0.
#        rts                    ;Now return to calling routine with the byte value.
#        nop                    ;Long word align code.
#        even                   ;Done!
#        end                    ;This will also compile with DevPac too!
# ; Yep, that's all there is to it... ;o)
#
# =============================================================================
#
# The binary, (peek), generated from the assembly code converted to text format using:-
# AMIGA_Prompt: C:Type HEX peek > peek.HEX<CR>
#
# The text HEX file representing the AMIGA executable to be edited...
# 0000: 000003F3 00000000 00000001 00000000    ...ó............
# 0010: 00000000 00000003 000003E9 00000003    ...........é....
# 0020: 4BF900F8 00001015 4E754E71 000003F2    Kù.ü....NuNq...ò
#
# =============================================================================
#
# This is the 256 byte ROM DUMP at address $00F80000...
#
# 0000: 11144EF9 00F800D2 0000FFFF 00280044    ..Nù.ø.Ò.....(.D
# 0010: 0028000A FFFFFFFF 00414D49 47412052    .(.......AMIGA R
# 0020: 4F4D204F 70657261 74696E67 20537973    OM Operating Sys
# 0030: 74656D20 616E6420 4C696272 61726965    tem and Librarie
# 0040: 7300436F 70797269 67687420 A9203139    s.Copyright © 19
# 0050: 38352D31 39393320 00436F6D 6D6F646F    85-1993 .Commodo
# 0060: 72652D41 6D696761 2C20496E 632E2000    re-Amiga, Inc. .
# 0070: 416C6C20 52696768 74732052 65736572    All Rights Reser
# 0080: 7665642E 00332E31 20524F4D 20006578    ved..3.1 ROM .ex
# 0090: 65632E6C 69627261 72790065 78656320    ec.library.exec 
# 00A0: 34302E31 30202831 352E372E 3933290D    40.10 (15.7.93).
# 00B0: 0A004E71 4E714AFC 00F800B6 00F8370E    ..NqNqJü.ø.¶.ø7.
# 00C0: 02280969 00F8008E 00F8009B 00F804AC    .(.i.ø...ø...ø.¬
# 00D0: 4E704FF8 040041FA FF2872FF 75017B00    NpOø..Aú.(r.u.{.
# 00E0: DA986402 528551C9 FFF851CA FFF44BFA    Ú.d.R.QÉ.øQÊ.ôKú
# 00F0: 001A41FA FF0C43F9 00F00000 B3C8670A    ..Aú..Cù.ð..³Èg.
#
# =============================================================================
#
# After finding the address of the string, ~find_this_text~ using the id()
# function, this was the RAM DUMP for Python Version 1.4.0 on my test machine.
#
# 0000: 00000002 002B8290 00000072 FFFFFFFF    .....+.....r....
# 0010: 57652077 696C6C20 75736520 74686520    We will use the 
# 0020: 69642829 2066756E 6374696F 6E20746F    id() function to
# 0030: 2066696E 64207468 6973206C 696E6520     find this line 
# 0040: 6C617465 722E2054 68652074 68696E67    later. The thing
# 0050: 2069732C 20796F75 2043414E 20646F20     is, you CAN do 
# 0060: 74686973 20776974 6820616E 20414D49    this with an AMI
# 0070: 47412057 4954484F 55542061 6E204D4D    GA WITHOUT an MM
# 0080: 5521004E 00000020 00000002 002B8290    U!.N... .....+..
# 0090: 0000000E 123E7734 66696E64 5F746869    .....>w4find_thi
# 00A0: 735F7465 78740008 00000000 00000019    s_text..........
# 00B0: 00000001 002B8290 00000007 FFFFFFFF    .....+..........
# 00C0: 64656670 61746800 0030494C 00000018    defpath..0IL....
# 00D0: 00000001 002B8290 00000006 FFFFFFFF    .....+..........
# 00E0: 73747269 6E67000F 00030030 0000001D    string.....0....
# 00F0: 00000001 002B8290 0000000B FFFFFFFF    .....+..........
#
# =============================================================================
#
# Again, finding the address of the string, ~find_this_text~ using the id()
# function, this was the RAM DUMP for Python Version 2.0.1 on my test machine.
#
# 0000: 00000002 0032956C 00000072 FBA7A5FC    .....2.l...rû§¥ü
# 0010: 00000000 57652077 696C6C20 75736520    ....We will use 
# 0020: 74686520 69642829 2066756E 6374696F    the id() functio
# 0030: 6E20746F 2066696E 64207468 6973206C    n to find this l
# 0040: 696E6520 6C617465 722E2054 68652074    ine later. The t
# 0050: 68696E67 2069732C 20796F75 2043414E    hing is, you CAN
# 0060: 20646F20 74686973 20776974 6820616E     do this with an
# 0070: 20414D49 47412057 4954484F 55542061     AMIGA WITHOUT a
# 0080: 6E204D4D 55210000 00000085 00000024    n MMU!.........$
# 0090: 00000004 0032956C 0000000E 123E7734    .....2.l.....>w4
# 00A0: 0038A16C 66696E64 5F746869 735F7465    .8¡lfind_this_te
# 00B0: 78740001 00000000 000000C8 00329DA8    xt.........È.2.š
# 00C0: 00000009 0038C10C 00000000 00000013    .....8Á.........
# 00D0: 01240000 00000000 00870000 00010038    .$.............8
# 00E0: A1C40123 0038A250 00000060 00000000    ¡Ä.#.8¢P...`....
# 00F0: 00870000 00010038 A1DC0000 0038A250    .......8¡Ü...8¢P
#
# =============================================================================

print "\f\n$VER: AMIGA_Peek_Mem.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU."
print "\nPlease wait..."

import os
import struct

find_this_text="We will use the id() function to find this line later. The thing is, you CAN do this with an AMIGA WITHOUT an MMU!"

# The only important _variable_.
global return_code
return_code=0

# Default to the start of the ROM, 0xF80000.
def peek(address=16252928):
	global return_code
	return_code=0
	# Don't allow any errors......
	address=int(address)
	# ......although this should NEVER occur...
	if address<=0: address=0
	# Limit to standard AMIGA A1200(HD) 16MB boundary for this DEMO.
	if address>=16777215: address=16777215
	# Generate the 32 bit address as a string...
	address_string=struct.pack("l",address)
	start_peek_string="\x00\x00\x03\xF3\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x03\xE9\x00\x00\x00\x03\x4B\xF9"
	end_peek_string="\x10\x15\x4E\x75\x4E\x71\x00\x00\x03\xF2"
	# Now create the AMIGA file that will be executed...
	peek_address_string=start_peek_string+address_string+end_peek_string
	# Generate the file inside the T: Volume, usually a RamDisk...
	amigafile=open("T:PeekMem","wb+")
	amigafile.write(peek_address_string)
	amigafile.close()
	# Ensure the file is executable; return_code is ignored here...
	return_code=os.system("C:Protect T:PeekMem rwed")
	# Run the AMIGA executable and get the return_code as a byte value...
	return_code=os.system("T:PeekMem")
	# We now have our byte read from memory _address_...
	return(return_code)

# Start of the DEMO using the peek() function.
# Do a single byte dump only for a start, it is effectively a Failat return code but
# it is redirected to the system's stderr so it is NOT seen on a default Python window...
print "\f\nFirstly, do a single byte dump at the AMIGA ROM address 16777215, $FFFFFF..."
address=16777215
return_code=peek(address)
print "\nByte value at the last odd address, $FFFFFF in the AMIGA ROM is "+str(return_code)+"...\n"

raw_input("Press <CR> to continue...")

# Access the function 256 times, this is slow, but hey, peeking memory by
# the back door cannot be bad, can it?
# Using the same address value as the default...
print "\f\nDo a 256 byte dump of the AMIGA ROM at the default address, $F80000..."
address=16252928
peeked_address=""
for n in range(address,(address+256),1):
	return_code=peek(n)
	peeked_address=peeked_address+chr(return_code)

# Generate the binary file as a file and autosave...
amigafile=open("T:Binary.BIN","wb+")
amigafile.write(peeked_address)
amigafile.close()

# Now convert to a text HEX version of the binary file inside the T: Volume.
os.system("C:Type HEX T:Binary.BIN > T:Binary.HEX")

# The return_code is directed to the system's stderr, so this ensures that
# the dump can be printed to the default Python window...
amigafile=open("T:Binary.HEX","r+")
peeked_address=amigafile.read()
amigafile.close()

# Print the dump to screen...
print "\f\nStart address of the 256 byte ROM dump is "+str(address)+", "+hex(address)+"...\n"
print peeked_address

raw_input("Press <CR> to continue...")

# Do the same again but this time find the _address_ of id(find_this_text)...
print "\f\nNow to find the address of the string _variable_ ~find_this_text~..."
address=id(find_this_text)
peeked_address=""
for n in range(address,(address+256),1):
	return_code=peek(n)
	peeked_address=peeked_address+chr(return_code)

amigafile=open("T:Binary.BIN","wb+")
amigafile.write(peeked_address)
amigafile.close()

os.system("C:Type HEX T:Binary.BIN > T:Binary.HEX")

amigafile=open("T:Binary.HEX","r+")
peeked_address=amigafile.read()
amigafile.close()

print "\f\nStart address of the 256 byte dump is "+str(address)+", "+hex(address)+"...\n"
print peeked_address+"\nEnd of the function, peek(), DEMO..."

# End of AMIGA_Peek_Mem.py DEMO.
# Enjoy finding simple solutions to often very difficult problems...
