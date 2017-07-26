# SimpleScope.py
# A standard text mode Python Audio LF Oscilloscope DEMO.
#
# (This working idea WILL become the basis of a Data-Logger/Transient-Recorder
# being worked on for Linux, Windows, Classic AMIGA and WinUAE using Arduino.)
#
# (Original working idea, (C)2010, B.Walker, G0LCU.)
# Now issued as Public Domian. You may do as you please with this code.
#
# To run type at the Python prompt:-
# >>> execfile('/full/path/to/file/SimpleScope.py')<RETURN/ENTER>
# Where "/full/path/to/file/" is the drawer(/folder/directory) that
# "SimpleScope.py" resides.
#
# For this DEMO /dev/dsp must exist for it to work, if not, then install
# oss-compat from your distro's repository.
# Ensure the sound system is not in use by another application.
#
# Tested on PCLinuxOS 2009, Knoppix 5.1.1, (and Debian 6.0.0 <- WITH
# oss-compat installed).
# "setterm" and "clear" are assumed to be available.
#
# This is the only import required for this working DEMO.
import os

def main():
	# Set everything as global for this DEMO.
	global ScopeScreen
	global ScopeWindow
	global audio
	global plot
	global position
	global horiz
	global record
	global grab

	# Allocate values.
	ScopeScreen="(C)2011, B.Walker, G0LCU."
	ScopeWindow="Simple LF Audio Oscilloscope."
	audio="/dev/dsp"
	plot=0
	position=67
	horiz=0
	record=" "
	grab=255

	# Turn off the cursor.
	os.system("setterm -cursor off")

	while 1:

		# This is the basic Osilloscope graticule window for this DEMO.
		ScopeScreen="+-------+-------+-------+-------+-------+-------+-------+--------+\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"|       |       |       |       +       |       |       |        |\n"
		ScopeScreen=ScopeScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+\n"

		# Save the this graticule window for further writing to.
		ScopeWindow=open("/tmp/ScopeScreen.txt","wb+")
		ScopeWindow.write(ScopeScreen)
		ScopeWindow.close()

		# Grab a string of 64 bytes in size at 8KHz sampling speed.
		# If you have an internal microphone just shout into it and
		# see a 4 bit depth waveform of you voice.
		# Alternatively feed a signal into the external mic input socket
		# and adjust the levels using the I/P and O/P volume control mixers.
		audio=file("/dev/dsp","rb")
		record=audio.read(64)
		audio.close()

		horiz=0
		ScopeWindow=open("/tmp/ScopeScreen.txt","rb+")
		while horiz<=63:
			# Convert each part of the record string into decimal.
			grab=ord(record[horiz])
			# Now convert to 4 bit depth for text mode display.
			plot=int(grab/16)
			# Invert to suit the text display window.
			plot=15-plot
			# Don't allow an error.
			if plot<=0: plot=0
			if plot>=15: plot=15
			# Set up the horizontal position and plot.
			position=68+horiz+plot*67
			ScopeWindow.seek(position)
			ScopeWindow.write("o")
			horiz=horiz+1

		# Now get the whole ScopeWindow with the plotted points......
		ScopeWindow.seek(0)
		ScopeScreen=ScopeWindow.read(1206)
		ScopeWindow.close()
		# ......and print it to the terminal window.
		print os.system("clear"),chr(13),"  ",chr(13),
		print ScopeScreen
		print "Simple Audio Oscilloscope DEMO using /dev/dsp in Linux."
		print "Ctrl-C to quit..."

	# Reset the cursor assuming it gets here... ;o)
	os.system("setterm -cursor on")
main()

# SimpleScope.py program end.
# Enjoy finding simple solutions to often very difficult problems.
