# AMIGA_HW.py
#
# DEMO Python code to switch the AMIGAs audio filter ON and OFF on the fly.
# It also changes the video mode to PAL or NTSC if required.
# (C)2007-2012, B.Walker, G0LCU. Now issued as Public Domain, you may do
# with it as you please.
#
# Written in such a way that almost anyone can understand how it works.
#
# For a minimum of a standard AMIGA A1200(HD) and Python 1.4.0, or for
# higher end AMIGAs to 2.0.1.
# Also WinUAE 1.5.3 minimum with Workbench 3.0.x and Python as above.
#
# Ensure that the assigned T: volume exists so as NOT to keep the file when
# the AMIGA is rebooted.
#
# Copy/drag this file into the PYTHON: volume and rename it AMIGA_HW.py.
# Call it from the Python prompt as:-
#
# >>> execfile("PYTHON:AMIGA_HW.py")<RETURN/ENTER>
#
# And away you go... ;o)
# ==========================================================================
# The assembly program that _defaults_ to audio filter ON condition, (when
# <RETURN/ENTER> is pressed only), and then compiled and converted.
# The address and control byte are changed as required before generating
# the executable file...
#
# From an AMIGA CLI using, a68k and blink, the executable AMIGA_Filter is
# created thus:-
# DRIVE:Path/To/Source> a68k AMIGA_Filter.asm<RETURN/ENTER>
# <Some reports here.>
# DRIVE:Path/To/Source> blink AMIGA_Filter.o
# <Some more reports here.>
# DRIVE:Path/To/Source> _
# ==========================================================================
# start:
#                                    ;Assembler source to switch the
#                                    ;audio filter and power light to ON.
#                                    ;Compiled under a68k and linked under blink.
#                                    ;A68k AMIGA_Filter<RETURN/ENTER>
#                                    ;<Some reports here.>
#                                    ;blink AMIGA_Filter.o<RETURN/ENTER>
#                                    ;<Some more reports here.>
#      move.b   #252,$BFE001         ;Set Audio Filter to bootup default condition ON.
#                                    ;Decimal 252, (0xFC), sets the filter to ON and
#                                    ;decimal 254, (0xFE), sets the filter to OFF.
#      clr.l    d0                   ;Set return code as OK.
#      rts                           ;Exit program.
#      end
# ==========================================================================
# The text HEX dump from the CLI using:-
# DRIVE:Path/To/Source> Type HEX AMIGA_Filter > AMIGA_Filter.txt<RETURN/ENTER>
# DRIVE:Path/To/Source> _
#
# Gives a text file, AMIGA_Filter.txt, with the contents thus...
# ==========================================================================
# 0000: 000003F3 00000000 00000001 00000000    ...ó............
# 0010: 00000000 00000003 000003E9 00000003    ...........é....
# 0020: 13FC00FC 00BFE001 42804E75 000003F2    .ü.ü.¿à.B.Nu...ò
# ==========================================================================
# To be edited to suit the Python code...
#
# Enjoy finding simple solutions to often very difficult problems...
#
# $VER: AMIGA_HW.py_Version_0.00.10_(C)2007-2012_B.Walker_G0LCU.

# The only STANDARD import required...
import os

def main():
	while 1:
		# A basic working screen to switch the audio filter mode....
		print("\f\nA simple Python hardware _controller_ for the Classic AMIGA A1200(HD).\n")
		print("(C)2007-2012, B.Walker, G0LCU. Now issued as Public Domain.\n")
		print("Press (f)<RETURN/ENTER> to enable audio filtering, (bootup default).")
		print("Press (F)<RETURN/ENTER> to disable audio filtering.")
		print("Press (p) or (P)<RETURN/ENTER> for PAL video mode.")
		print("Press (n) or (N)<RETURN/ENTER> for NTSC video mode.")

		# Set to the audio filter address and to ON by default.
		control_byte="\xFC"
		hw_address="\x00\xBF\xE0\x01"
		keyboard=raw_input("Press (q) or (Q)<RETURN/ENTER> to Quit:- ")
		if keyboard=="f" or keyboard==chr(13):
			control_byte="\xFC"
			hw_address="\x00\xBF\xE0\x01"
		if keyboard=="F":
			control_byte="\xFE"
			hw_address="\x00\xBF\xE0\x01"
		if keyboard=="p" or keyboard=="P":
			control_byte="\x20"
			hw_address="\x00\xDF\xF1\xDC"
		if keyboard=="n" or keyboard=="N":
			control_byte="\x00"
			hw_address="\x00\xDF\xF1\xDC"
		if keyboard=="Q" or keyboard=="q" or keyboard==chr(27): break

		# Manually place the binary into a string format for Python 1.4.0 to 2.0.1.
		binary_one="\x00\x00\x03\xF3\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x03\xE9\x00\x00\x00\x03\x13\xFC\x00"
		binary_two="\x42\x80\x4E\x75\x00\x00\x03\xF2"

		# Create the running file and place it into the AMIGA T: volume as AMIGA_HW.
		amiga_exe_file=binary_one+control_byte+hw_address+binary_two
		amigafile=open("T:AMIGA_HW","wb+")
		amigafile.write(amiga_exe_file)
		amigafile.close()

		# Give a short delay to allow system to settle.
		os.system("C:Wait 1")

		# Ensure the file AMIGA_HW can be executed.
		os.system("C:Protect T:AMIGA_HW rwed")

		# Now run it and _immediately_ re-run this code...
		os.system("T:AMIGA_HW")
main()
# End of AMIGA_HW.py.
# Enjoy finding simple solutions to often very difficult problems...
