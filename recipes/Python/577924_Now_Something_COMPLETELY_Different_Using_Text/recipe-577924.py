# AC2DC.py
#
# This is a demo to show the power of the audio hardware under the
# influence of standard text mode Python.
#
# (C)2010, B.Walker, G0LCU. Now issued as Public Domain; you may do
# with this code as you please.
#
# Tested on PCLinuxOS 2009 and Debian 6.0.0 using Python 2.5.2, 2.6.6
# and 2.7.2; (it may well work on Python versions earlier than the
# above but it is untested).
#
# The device "/dev/dsp" is needed for this to work so you might have
# to install "oss-compat" from your distribution's repository...
#
# A very simple voltage doubler and passive filter TEST CIRCUIT ONLY...
# Best viewed in pure text mode.
# (Connect DC OUT & GND to a DC coupled oscilloscope to see it working.)
#
# Headset O/P. C1.             |\|D2.
#  O--------o--||--o-------o---| +---o-------o-------O +VE DC OUT.
#           |      |       |   |/|+  |       |
#  O       <       | +    <          |      <
#  |         >   --+--      >        | +      >
#  | * R1. <      / \ D1. <  R2.    === C2. <  R3.
#  |         >   +---+      >        |        >
#  |       <       |      <          |      <
#  |        |      |       |         |       |
#  +--------o------o-------o---------o---o---o-------O -VE.
#                                        |
# Parts List.                         ---+--- GND.
# -----------                         ///////
# C1 = 1.0 uF, 50V.
# C2 = 10 uF, electrolytic, 10V.
# R1 = 47 KilOhms, (* this can be ommitted).
# R2 = 1 MegOhm.
# R3 = 100 KilOhms.
# D1, D2 = OA90 or any similar germanium diode.
# 3.2 mm stereo jack plug for headset socket.
# Coaxial connecting cable.
# Sundries as required, stripboard, etc.

import os
# The running code...
def main():
	# Set globals, my choice... ;o)
	global waveform
	global value
	global count
	# Choose startup values...
	waveform=chr(0)+chr(0)
	value="(C)2010, B.Walker, G0LCU."
	count=0
	while 1:
		# Use the Linux system clear-screen command.
		os.system("clear")
		# A simple user screen...
		print "\nA DEMO variable AC to DC Generator using the sound card in Linux.\n"
		print "(C)2010, B.Walker, G0LCU; now issued as Public Domain...\n"
		value=raw_input("Input any integer from 0 to 255, [RETURN/ENTER] to Quit:- ")
		# Don't allow any errors...
		if value=="": break
		if len(value)>=4: value="255"
		count=0
		while count<=(len(value)-1):
			if value[count]>=chr(48) and value[count]<=chr(57): count=count+1
			else: value="255"
		if int(value)>=255: value="255"
		if int(value)<=0: value="0"
		# Create a symetrical triangle waveform with an amplitude of "value".
		print "\nOutput level value is "+value+"..."
		waveform=chr(0)+chr(int(value))
		# Generate this signal for about 10 seconds for this DEMO.
		if int(value)>=1:
			count=0
			audio=open("/dev/dsp", "wb")
			while count<=40000:
				audio.write(waveform)
				count=count+1
			audio.close()
main()
# End of AC2DC.py program.
# Enjoy finding simple solutions to often very difficult problems... ;o)
