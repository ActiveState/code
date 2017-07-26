# Ami_Square_Wave.py
#
# DEMO to generate an audio tone from one of the classic AMIGA audio
# channels, in this case a square wave. Almost any waveform is possible
# and the Left Mouse Button is used to STOP this DEMO.
#
# MINIMUM Requirements Are:-
# 68EC020 CPU and 2MB RAM total, example, a standard A1200(HD),
# WinUAE and E-UAE. Standard AMIGA OS3.0x install or better.
# Full Python 1.4.0, minimum, installed, can be found on AMINET.
# (Python 1.5.2 to 2.0.x are also available on AMINET.)
# (Now Python 2.4.6 is available for advanced 68K machines.)
#
# To install just download the file and drag this file into an Assign(ed)
# PYTHON: volume...
# From an AMIGA A1200(HD), E-UAE or WinUAE Python 1.4.0 prompt:-
#
# >>> execfile("PYTHON:Ami_Square_Wave.py")
#
# And away you go...
# ==========================================================================
# The DEMO assembly code that will be compiled and converted.
# Call the code beep.asm...
# From a CLI and using the a68k and blink from AMINET:-
#
# Prompt> a68k beep.asm<RETURN/ENTER>
# Some reports here...
# Prompt> blink beep.o<RETURN/ENTER>
# Some reports here...
#
# This code is TOTALLY, even address, position independent.
# ==========================================================================
# start:
#					;"beep.asm" test code...
#	movem.l	d0-d7/a0-a6,-(sp)	;Save all registers just in case.
#	movea.l	$4,a6			;Set ~execbase~.
#	moveq	#16,d0			;Length of square wave data.
#	moveq	#2,d1			;Set to chip ram.
#	jsr	-198(a6)		;Allocate memory for the task.
#	beq.s	getout			;On error, Quit.
#	move.l	d0,a0			;Set address in chip ram.
#	move.l	#$3f3f3f3f,(a0)		;Set first four bytes of sixteen.
#	addq.l	#4,a0			;Move addres by four.
#	move.l	#$3f3f3f3f,(a0)		;Set next four bytes of sixteen.
#	addq.l	#4,a0			;Move addres by four.
#	move.l	#$80808080,(a0)		;Set next four bytes of sixteen.
#	addq.l	#4,a0			;Move addres by four.
#	move.l	#$80808080,(a0)		;Set last four bytes of sixteen.
#					;This ensures absolute position
#					;independence.
#	lea	$dff000,a5		;Set HW register base.
#	move.w	#$000f,$96(a5)		;Disable audio DMA.
#	move.l	d0,$a0(a5)		;Set address of audio data.
#	move.w	#8,$a4(a5)		;Set length in words.
#	move.w	#64,$a8(a5)		;Set volume to maximum.
#	move.w	#220,$a6(a5)		;Set the period.
#	move.w	#$00ff,$9e(a5)		;Disable any modulation.
#	move.w	#$8201,$96(a5)		;Enable audio DMA, 1 channel only.
# wait:
#	btst	#6,$bfe001		;If LMB pressed then Quit.
#	beq.s	closeme			;Do it.
#	bne.s	wait			;Play the tone until LMB pressed...
# closeme:
#	move.w	#$000f,$96(a5)		;Disable audio DMA.
#	move.l	d0,a0			;Address of the square wave data.
#	moveq	#16,d0			;The data length to recover.
#	jsr	-210(a6)		;Free assigned memory.
# getout:
#	movem.l	(sp)+,d0-d7/a0-a6	;Restore all registers.
#	clr.l	d0			;Set returm code OK.
#	rts
#	nop
#	even
#	end
# ==========================================================================
# The text HEX file to be edited for the Python code:-
#
# Prompt> Type HEX beep > beep.hex<RETURN/ENTER>
#
# Gives a text file "beep.hex" that has the contents:-
# ==========================================================================
# 0000: 000003F3 00000000 00000001 00000000    ...ó............
# 0010: 00000000 00000021 000003E9 00000021    .......!...é...!
# 0020: 48E7FFFE 2C780004 70107202 4EAEFF3A    Hç.þ,x..p.r.N®.:
# 0030: 67682040 20BC3F3F 3F3F5888 20BC3F3F    gZ @ Œ????X. Œ??
# 0040: 3F3F5888 20BC8080 80805888 20BC8080    ??X. Œ....X. Œ..
# 0050: 80804BF9 00DFF000 3B7C000F 00962B40    ..Kù.ßð.;|....+@
# 0060: 00A03B7C 000800A4 3B7C0040 00A83B7C    . ;|...€;|.@.š;|
# 0070: 00DC00A6 3B7C00FF 009E3B7C 82010096    .Ü.Š;|....;|....
# 0080: 08390006 00BFE001 670266F4 3B7C000F    .9...¿à.g.fô;|..
# 0090: 00962040 70104EAE FF2E4CDF 7FFF4280    .. @p.N®..Lß..B.
# 00A0: 4E754E71 000003F2                      NuNq...ò
# ==========================================================================
# With careful manipulation of the Python code you could have control of the
# audio levels, channels, frequency, etc, using this method...
#
# Enjoy finding simple solutions to often very difficult problems...
#
# $VER: Ami_Square_Wave.py_Version_0.00.30_(C)2007-2011_B.Walker_G0LCU.
#
# Original copyright, (C)2007-2011, B.Walker, G0LCU. Now finally issued as Public Domain.

import os

# Manually place the executable code into practical binary string lengths.
one="\x00\x00\x03\xF3\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x21\x00\x00"
two="\x03\xE9\x00\x00\x00\x21\x48\xE7\xFF\xFE\x2C\x78\x00\x04\x70\x10\x72\x02\x4E\xAE\xFF\x3A\x67\x68\x20\x40\x20\xBC"
wave="\x3F\x3F\x3F\x3F\x58\x88\x20\xBC\x3F\x3F\x3F\x3F\x58\x88\x20\xBC\x80\x80\x80\x80\x58\x88\x20\xBC\x80\x80\x80\x80"
three="\x4B\xF9\x00\xDF\xF0\x00\x3B\x7C\x00\x0F\x00\x96\x2B\x40\x00\xA0\x3B\x7C\x00\x08\x00\xA4\x3B\x7C\x00"
volume="\x40"
four="\x00\xA8\x3B\x7C\x00\xDC\x00\xA6\x3B\x7C\x00\xFF\x00\x9E\x3B\x7C\x82\x01\x00\x96\x08\x39\x00\x06\x00\xBF"
five="\xE0\x01\x67\x02\x66\xF4\x3B\x7C\x00\x0F\x00\x96\x20\x40\x70\x10\x4E\xAE\xFF\x2E\x4C\xDF\x7F\xFF\x42\x80"
six="\x4E\x75\x4E\x71\x00\x00\x03\xF2"

# Clear the screen the standard AMIGA way... ;o)
print "\f"

# A simple user screen...
print "1 KHz Square Wave Generator for the classic AMIGA A1200."
print "Using standard text mode Python 1.4.0 to 2.0.1.\n"
print "(C)2007-2011, B.Walker, GOLCU. Issued as Public Domain...\n"

# Show how to change output, (volume), level...
vol=raw_input("Set output level, 0 to 64:- ")

# Don't allow any errors...
if vol=="": vol="64"
if len(vol)>=3: vol="64"
count=0
while count<=(len(vol)-1):
	if vol[count]>=chr(48) and vol[count]<=chr(57): count=count+1
	else: vol="64"
if eval(vol)>=64: vol="64"
if eval(vol)<=0: vol="0"
volume=chr(eval(vol))

# Put them all together as a single binary string.
amiga_exe_file=one+two+wave+three+volume+four+five+six

# Generate a file called SquareWave inside the S: VOLUME and write to the disk.
amigafile=open("S:SquareWave","wb+")
amigafile.write(amiga_exe_file)
amigafile.close()

# Give a short delay to allow system to settle.
os.system("C:Wait 1")

print "\nPress Left Mouse Button to stop...\n"

# Ensure the file SquareWave can be executed.
os.system("C:Protect S:SquareWave rwed")

# Now run it.
os.system("S:SquareWave")
print "This DEMO has now stopped..."

# Ami_Square_Wave.py end...
# Enjoy finding simple solutions to often very difficult problems.
