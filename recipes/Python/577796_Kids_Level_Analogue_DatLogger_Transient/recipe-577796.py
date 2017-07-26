# DataLogger.py
#
# Copyright, (C)2011, B.Walker, G0LCU.
#
# Issued under the MIT licence.
#
# A kids level project using the Arduino Diecimila and other related boards as an
# analogue input for use as a Data Logger using Python in text mode only. The accuarcy
# is 8 bit depth but the display is only 4 bit depth due to the limitations of text mode.
#
# This is the second feeder upload, it is nowhere near completion. ANY future uploads
# will no longer be feeders.
#
# This code defaults to DEMO mode but the crucial Arduino code is added and just
# requires the line "demo=0" to access the board and the correct device number to
# be changed. Later versions of Arduino now use /dev/ttyACMx in Linux and I have
# not got one to test with, so if any of you guys are willing to experiment by
# changing the Linux device type and number and let me know how you get on with
# it, then thanks.
#
# It now auto-saves a file after every 64 plots in CSV format and tested on MS Works
# and Open Office Org, read the code for more information. To disable the auto-save feature
# just set it to, "autosave=0"...
#
# The test *.pde file for the Arduino Diecimila Board is here:-
#
# http://code.activestate.com/recipes/577625-arduino-diecimila-board-access-inside-winuae-demo/?in=user-4177147
#
# Tested on Windows XP using Python 2.4.2, Vista using Python 2.6.1, PCLinuxOS 2009 using
# Python 2.5.2, Debian Linux using Python 2.6.6 and 2.7.2, a stock AMIGA A1200 using
# Python 1.4.0 and WinUAE with standard AMIGA OS 3.1 using Python 2.0.1.
# I have no idea whether this works on Windows 7 or MAC OSX as I have not got either.
# DEMO mode ONLY works in E-UAE with standard AMIGA OS 3.1 and Python 1.4.0 or Python 2.0.1.
#
# IMPORTANT NOTE:- The Linux platforms assume running Python from a root default Terminal in NONE DEMO mode.
#
# (Version set in Classic AMIGA format... ;o)
# $VER: DataLogger.py_Version_0.00.20_(C)2011_B.Walker_G0LCU.

# Imports required so far...
import sys
import os
import random
import time

def main():
	# Deliberately set all parameters as global, (my choice!).
	global LoggerScreen
	global MyFiles
	global savefile
	global plot
	global position
	global horiz
	global demo
	global pause
	global pausestring
	global serialport
	global mybyte
	global grab
	global csvdata
	global autosave
	global filestr
	# global n
	# initial parameter settings...
	LoggerScreen="(C)2011, B.Walker, G0LCU."
	MyFiles="Data_Logger-Transient_Recorder."
	savefile="/tmp/LoggerStartup.txt"
	# Default DEMO mode, set to 0 for REAL mode.
	demo=1
	plot=0
	horiz=1
	position=79
	pause=1
	pausestring="1"
	# The latest Linux device name for current Arduino variants, (01-01-2011).
	serialport="/dev/ttyACM0"
	mybyte="?"
	grab=255
	csvdata="?"
	# Temporarily set to autosave enabled for testing, set to 0 to disable.
	autosave=1
	filestr="0000000000.CSV"
	# n=0

	# Determine AMIGA, Windows-(32 bit), WinUAE or Linux for serial access.
	if sys.platform=="amiga":
		# The AMIGA serial port may need to be changed to 1200 baud, no parity,
		# 8 bit data and 1 stop bit, this applies to WinUAE too.
		serialport="SER:"
	if sys.platform=="linux2":
		# Assumed running from root for the time being.
		# /dev/ttyUSB0 the device on my test systems, the Arduino Diecimila Board.
		# It may need to be changed for your needs.
		serialport="/dev/ttyUSB0"
		os.system("chmod 666 "+serialport)
		os.system("stty -F "+serialport+" 1200")
		os.system("stty -F "+serialport+" raw")
	if sys.platform=="win32":
		# This is the COM port number generated on a test system.
		# It may need to be changed for your needs.
		serialport="COM3:"
		os.system("MODE "+serialport+" BAUD=1200 PARITY=N DATA=8 STOP=1 to=on")

	# A clear screen function for the platforms shown.
	def clrscn():
		if sys.platform=="amiga": print "\f",
		if sys.platform=="linux2": print os.system("clear"),chr(13),"  ",chr(13),
		if sys.platform=="win32": print os.system("CLS"),chr(13),"  ",chr(13),

	# Save the initial screen for future use function.
	def savescreen():
		global MyFiles
		global savefile
		global LoggerScreen
		if sys.platform=="amiga": savefile="S:LoggerStartup.txt"
		if sys.platform=="linux2": savefile="/tmp/LoggerStartup.txt"
		if sys.platform=="win32": savefile="C:\\Windows\\Temp\\LoggerStartup.txt"
		MyFiles=open(savefile,"wb+")
		MyFiles.write(LoggerScreen)
		MyFiles.close()

	# This function does the plotting and generates a text variable in CSV format.
	# It also sets the timebase values as required, not implimented yet.
	def doplot():
		global horiz
		global position
		global savefile
		global MyFiles
		global LoggerScreen
		global demo
		global pause
		global pausestring
		global plot
		global mybyte
		global serialport
		global grab
		global csvdata
		csvdata=""
		horiz=1
		while horiz<=64:
			# Generate a byte as though grabbed from Arduino.
			if demo==1: grab=int(random.random()*256)
			# Generate a byte from Arduino.
			if demo==0:
				MyFiles=open(serialport,"rb",2)
				mybyte=str(MyFiles.read(1))
				MyFiles.close()
				# Convert to a decimal value, assume 8 bit integer.
				grab=ord(mybyte)
			# Generate the 64 byte CSV string on the fly...
			csvdata=csvdata+str(grab)+"\r\n"
			# Convert to 4 bit depth.
			plot=int(grab/16)
			# Invert to suit the text display window.
			plot=15-plot
			if plot<=0: plot=0
			if plot>=15: plot=15
			# Set up the plot position per grab.
			position=79+horiz+plot*79
			MyFiles=open(savefile,"rb+")
			MyFiles.seek(position)
			MyFiles.write("o")
			# Now get the whole array.
			MyFiles.seek(0)
			LoggerScreen=MyFiles.read(1659)
			MyFiles.close()
			# End of screen array update per plot.
			# Wait for a period for none AMIGA platforms.
			if sys.platform!="amiga": time.sleep(pause)
			# time.sleep() does NOT work on an A1200, WinUAE and E-UAE so pause......
			if sys.platform=="amiga":
				pausestring=str(pause)
				os.system("C:Wait "+pausestring)
				# ......and then do a clear screen.
				print "\f",
			# Do a clear screen for other platforms.
			if sys.platform=="linux2": print os.system("clear"),chr(13),"  ",chr(13),
			if sys.platform=="win32": print os.system("CLS"),chr(13),"  ",chr(13),
			# Now print the whole on screen...
			print LoggerScreen
			horiz=horiz+1

	# This function saves a file to disk every 64 plots in CSV format.
	def datafile():
		global MyFiles
		global filestr
		global savefile
		filestr=str(int(time.time()))+".CSV"
		if sys.platform=="amiga": savefile="S:"
		if sys.platform=="linux2": savefile="/tmp/"
		if sys.platform=="win32": savefile="C:\\Windows\\Temp\\"
		savefile=savefile+filestr
		MyFiles=open(savefile,"wb+")
		MyFiles.write(csvdata)
		MyFiles.close()

	# This is the main running code.
	while 1:
		# Set up DataLogger screen, use "\r\n" to suit Windows, "\r" is *ignored* on Linux and AMIGA_OS.
		# This is for the default Command Prompt, (Windows), Terminal, (Linux) and CLI, (AMIGA), modes.
		LoggerScreen="+-------+-------+-------+-------+-------+-------+-------+--------+ +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | |>(R)UN  |\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+ | Ctrl-C |\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | | (K)B   |\r\n"
		LoggerScreen=LoggerScreen+"+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++ +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | | (S)LOW |\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +---------\r\n"
		LoggerScreen=LoggerScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+ +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | | 1(0)S  |\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | +--------+\r\n"
		LoggerScreen=LoggerScreen+"|       |       |       |       +       |       |       |        | |>(1)S   |\r\n"
		LoggerScreen=LoggerScreen+"+-------+-------+-------+-------+-------+-------+-------+--------+ +--------+\r\n"
		LoggerScreen=LoggerScreen+"+----------------------------------------------------------------+ +--------+\r\n"
		LoggerScreen=LoggerScreen+"| Status:- Running in DEMO mode.                                 | | (U)NCAL|\r\n"
		LoggerScreen=LoggerScreen+"+----------------------------------------------------------------+ +--------+\r\n"

		# Save the startscreen to write to.
		savescreen()
		# Clear the screen every 64 plots and restart.
		clrscn()
		print LoggerScreen
		# Grab the 64 plots.
		doplot()
		# Automatically save to disk when autosave is set to 1.
		if autosave==1: datafile()

main()

# DataLogger program end.
# Enjoy finding simple solutions to often very difficult problems.
