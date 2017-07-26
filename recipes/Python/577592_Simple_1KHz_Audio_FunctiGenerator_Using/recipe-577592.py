# Audio Function Generator; "afg.py"...
# -------------------------------------
#
# A fun Python program to generate a Sine, Square, Triangle, Sawtooth,
# and Pulse waveforms using STANDARD Python at the earphone sockets.
# This is for (PC)Linux(OS), (ONLY?), and was done purely for fun.
# (It has now been tested on Debian 6.0.0 and Knoppix 5.1.1!)
#
# Although it is fairly easy to alter the frequency within limits I
# have left it at approximately 1KHz to keep the code size down...
#
# It would be tricky to change the output level using STANDARD Python
# for (PC)Linux(OS) 2009 using this idea to generate waveforms, but it
# is possible within limits.
#
# (Original idea copyright, (C)2009, B.Walker, G0LCU.)
# Issued as Public Domain, (to LXF) and you may do with it as you please.
#
# It is assumed that /dev/audio exists; if NOT, then install oss-compat
# from the distro`s repository.
#
# Ensure the sound system is not already in use.
#
# Copy the file to the Lib folder(/drawer/directory) or where the modules
# reside as "afg.py"...
#
# For a quick way to run just use at the ">>>" prompt:-
#
# >>> import afg[RETURN/ENTER]
#
# And away we go...
#
# The waveforms generated are unfiltered and therefore not "pure",
# but hey, an audio function generator signal source, for free, without
# external hardware, AND, using standard Python, what more do you want... :)
#
# Using my notebook about 150mV p-p was generated at the earphone
# socket(s).
#
# Coded on a(n) HP dual core notebook running PCLinuxOS 2009 and
# Python 2.5.2 for Linux...
#
# You will need an oscilloscope connected to the earphone socket(s)
# to see the resultant waveform(s) generated, or listen to the
# harshness of the sound... ;o)
#
# It is EASILY possible to generate pseudo-random noise also but
# I'll leave that for you to work out... :)

# Import any modules...
import os

# Clear a terminal window ready to run this program.
print os.system("clear"),chr(13),"  ",chr(13),

# The program proper...
def main():
	# Make all variables global, a quirk of mine... :)
	global sine
	global square
	global triangle
	global sawtoothplus
	global sawtoothminus
	global pulseplus
	global pulseminus
	global waveform
	global select
	global count

	# Allocate values to variables.
	# Any discrepancy between random soundcards may require small changes
	# in the numeric values inside each waveform mode...
	# These all oscillate at around 1KHz.
	sine=chr(15)+chr(45)+chr(63)+chr(45)+chr(15)+chr(3)+chr(0)+chr(3)
	square=chr(63)+chr(63)+chr(63)+chr(63)+chr(0)+chr(0)+chr(0)+chr(0)
	triangle=chr(0)+chr(7)+chr(15)+chr(29)+chr(63)+chr(29)+chr(15)+chr(7)
	sawtoothplus=chr(63)+chr(39)+chr(26)+chr(18)+chr(12)+chr(8)+chr(4)+chr(0)
	sawtoothminus=chr(0)+chr(4)+chr(8)+chr(12)+chr(18)+chr(26)+chr(39)+chr(63)
	pulseplus=chr(0)+chr(63)+chr(63)+chr(63)+chr(63)+chr(63)+chr(63)+chr(63)
	pulseminus=chr(63)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0)+chr(0)

	# This is the INITIAL default waveform, the Square Wave.
	waveform=square
	select="G0LCU."
	count=1

	# A continuous loop to change modes as required...
	while 1:
		# Set up a basic user window.
		print os.system("clear"),chr(13),"  ",chr(13),
		print
		print "Simple Function Generator using STANDARD Python 2.5.2"
		print "for PCLinuxOS 2009, issued as Public Domain to LXF..."
		print
		print "Original idea copyright, (C)2009, B.Walker, G0LCU."
		print
		print "1) Sinewave."
		print "2) Squarewave."
		print "3) Triangle."
		print "4) Positive going sawtooth."
		print "5) Negative going sawtooth." 
		print "6) Positive going pulse."
		print "7) Negative going pulse."
		print "Q) or q) to quit..."
		print
		# Enter a number for the mode required.
		select=raw_input("Select a number/letter and press RETURN/ENTER:- ")
		if select=="": select="2"
		if len(select)!=1: break
		if select=="Q": break
		if select=="q": break
		if select=="1": waveform=sine
		if select=="2": waveform=square
		if select=="3": waveform=triangle
		if select=="4": waveform=sawtoothplus
		if select=="5": waveform=sawtoothminus
		if select=="6": waveform=pulseplus
		if select=="7": waveform=pulseminus
		# Re-use the variable ~select~ again...
		if select<=chr(48): select="Default OR last"
		if select>=chr(56): select="Default OR last"
		if select=="1": select="Sine wave"
		if select=="2": select="Square wave"
		if select=="3": select="Triangle wave"
		if select=="4": select="Positive going sawtooth"
		if select=="5": select="Negative going sawtooth"
		if select=="6": select="Positive going pulse"
		if select=="7": select="Negative going pulse"
		print os.system("clear"),chr(13),"  ",chr(13),
		print
		print select+" audio waveform generation..."
		print
		# Open up the audio channel(s) to write directly to.
		audio=file('/dev/audio', 'wb')
		# Make the tone generation time finite in milliseconds...
		# A count of 10000 is 10 seconds of tone burst...
		count=0
		while count<10000:
			# Write the waveform to the audio device.
			audio.write(waveform)
			count=count+1
		# Close the audio device when finished.
		audio.close()
main()

# End of demo...
# Enjoy finding simple solutions to often very difficult problems...
