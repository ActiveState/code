# ParOpenAMIGA.py
# ---------------------------------------------------------------------------
# Accessing the parallel port to import 8 bit data, (C)2006, B.Walker, G0LCU.
# This is now Public Domain. AMIGA-heads may do with it as they please. :)
# ---------------------------------------------------------------------------
# A DEMO stand alone running program that will obtain a single byte of data
# from a classic STOCK AMIGA A1200 parallel port and display the value on
# screen in decimal.
# ---------------------------------------------------------------------------
# The Python version for my STOCK A1200 was only V1.4 but was more than
# adequate for this exercise as it shows how EXTREMELY powerful PAR: is when
# used as a VOLUME. There are Python versions to 2.4.6 for the 680x0 family
# of classic AMIGA computers up on AMINET...
# http://main.aminet.net/
# ---------------------------------------------------------------------------
# PAR_READ.lha from the /docs/hard drawer of AMINET IS REQUIRED for this to
# work because PAR: used as a VOLUME HAS to have the -ACK line, Pin 10 of
# the parallel port, toggled continuously...
# http://aminet.net/package/docs/hard/PAR_READ
# ---------------------------------------------------------------------------
# STOCK AMIGA A1200, OS3.0x and topaz.font 8 were used for this program.
# ---------------------------------------------------------------------------

# Set up a version number recognised by the AMIGAs version command.
version = '$VER: ParOpen.py_V1.00.00_(C)15-01-2006_B.Walker_G0LCU.'

# Set up a basic screen, NOTE:- ~print '\f'~ is used as the CLS command.
print '\f'
print '           ',version
print
print '           Parallel Port access on the AMIGA using PAR: as a VOLUME.'
print
print '                            Press Ctrl-C to stop.'
print
print '               The decimal value at the parallel port is:- 0 .'

# This is the start of the continuous loop to grab the data sitting on the
# parallel port. It does about 2 samples per second and there IS a flaw here.
# It is NOT a bug however...
def main():

	while 1:
		# -----------------------------------------------------------
		# Set a pointer to the PAR: device and OPEN it up.
		pointer = open('PAR:', 'rb', 1)
		# Once set, grab my byte and ~store~ it.
		mybyte = str(pointer.read(1))
		# As soon as my byte is grabbed CLOSE down PAR:.
		pointer.close()
		# ===========================================================
		# Over print the printed line AND convert mybyte to a decimal value.
		print '\v','               The decimal value at the parallel port is:-',ord(mybyte),'.    '
		# Ctrl-C is used for stopping the program, or set all DATA lines to 1.
		# -----------------------------------------------------------
		if mybyte == chr(255): break
		# -----------------------------------------------------------

main()

# End of DEMO.
# Enjoy finding simple solutions to often very difficult problems... ;o)
