# DC_IN.py
#
# This DEMO shows how to get DC, (Direct Current), into a computer without
# the need for Integrated Cirduits, USB, Serial, Parallel etc, etc...
# It is used in this code as a very simple Logic Probe that will give some
# indication of a Logic 0, 1 or indeterminate. Only the external microphone input
# is required. "/dev/dsp" IS required so install "oss-compat" from your distro's
# repository if you do not have "/dev/dsp"...
# Ensure the sound system is not in use, and, use the OS's mixing facilities to
# set any input and output levels...
# Tested on Debian 6.0.0 using Python 3.1.3 and PCLinuxOS 2009 using Python 3.2.2.
# (C)2010, B.Walker, G0LCU. Now issued as Public Domain.
# Written in such a way that anyone can understand how it works.
#
# A very simple VCO, (Voltage COntrolled Oscillator), can be found here...
#
# http://www.4qdtec.com/mvbz/vco2.gif
#
# Assume a supply rail of 5 Volts to the VCO along with the circuit of the probe below...
#
# +5 Volt rail on VCO, (Vcc).
#  O-------------------------+
#                            |
#                            | +
#                          --+--
#                       D2. / \
#                          +---+
#                            |
# 1-4 Volt VCO I/P, (Vc).    |
#  O--------o---/\/\/\---o---o---/\/\/\---0 Probe I/P.
#           |     R2.    |         R3.
#  O       <             | +
#  |         >         --+--
#  |   R1. <            / \ D1.
#  |         >         +---+
#  |       <             |
#  |        |            |
#  +--------o------------o-------o--------O -VE.
# 0 Volts.                       |
#                             ---+--- GND.
# Parts List.                 ///////
# -----------
# R1 = 1 MegOhm.
# R2, R3 = 470 Ohms.
# D1, D2 = 1N4148 Diodes.
# All tolerances are wide open.
# Sundries, stripboard, wire, etc...

def main():
	# Make variables global; my choice... ;o)
	global record
	global n
	global freq
	global logic
	global LED
	global colour
	# Set the startup values...
	freq=0
	record=b"?"
	n=0
	logic="0"
	# Use "H" for this DEMO although the commented out "LED" may look better.
	LED="H"
	# LED=chr(0x2588)
	colour="\033[1;32m"
	while 1:
		# Do a 1 second recorded burst...
		audio=open('/dev/dsp', 'rb')
		# "record" is the "binary string" to be counted...
		record=audio.read(8000)
		audio.close()
		# Enter another loop to do the count...
		n=0
		freq=0
		while 1:
			# A VCO with a mark to space ratio of 1 to 1 will be used for this DEMO,
			# so "wait" until a "space" is found.
			# (For those that don't know.)
			#
			#                  +------+      +---
			# Square wave:-    | Mark |Space |
			#               ---+      +------+
			#
			# This ensures that the loop cycles when NO input is
			# applied to the microphone socket.
			# Exit this loop when "mark" is found or n>=8000...
			while record[n]<=127:
				n=n+1
				# Ensure as soon as n>=8000 occurs it drops out of the loop.
				if n>=8000: break
			# Ensure as soon as n>=8000 occurs it drops completely out of this loop.
			if n>=8000: break
			# Now the "mark" can loop until a "space" is found again and the whole
			# can cycle until n>=8000...
			while record[n]>=128:
				n=n+1
				# Ensure as soon as n>=8000 occurs it drops out of the loop.
				if n>=8000: break
			# Ensure as soon as n>=8000 occurs it drops completely out of this loop.
			if n>=8000: break
			# "freq" will become the frequency of a symmetrical waveform
			# when the above loops are finally exited, n>=8000...
			# Tick up the freq(uency) per "mark to space" cycle.
			freq=freq+1
			# Just 3 levels are displayed here but with more "if" statements much more
			# accuracy and range is easily possible. Also "look up tables" could be used if desired...
			# Set colour to Green for Logic 0, Red for Logic 1 and Yellow for indeterminate.
			# Logic 1 is approximately greater than 4 Volts.
			if freq>=3000:
				logic="1"
				# Red...
				colour="\033[1;31m"
			# Logic 0 is approximately less than 1 Volt.
			if freq<=300:
				logic="0"
				# Green...
				colour="\033[1;32m"
			# Indeterminate is between 1 and 4 Volts and/or a slow oscillation being measured...
			if freq>=301 and freq<=2999:
				logic="indeterminate"
				# Yellow...
				colour="\033[1;33m"
		# An ultra simple clear screen line...
		# This line is not needed for the demo but added for fullness...
		print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
		# Now display the value in the same place on screen every time.
		# This assumes a 24 or 25 line Python Shell window. Just modify to
		# suit your particular Shell that you use...
		print("\033[0m\nSimple DC Input in the guise of a TTL level Logic Probe.\n")
		print("(C)2010-2011, B.Walker, G0LCU. Issued as Public Domain.\n\n\n")
		# Print a large coloured square "LED" for quick and easy viewing.
		for n in range (0,3,1):
			print("                                     "+colour+LED+LED+LED+LED+LED+LED)
		print("\033[0m\n\n\nLogic level is "+colour+logic+"\033[0m...\n\n\n\n\n\n\n\n\n")
main()
# End of DC_IN.py DEMO.
# Enjoy finding simple solutions to often very difficult problems.
