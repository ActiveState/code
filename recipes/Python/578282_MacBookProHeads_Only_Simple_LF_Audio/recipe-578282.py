# SimpleScope_OSX.py
# A standard text mode Python Audio LF Oscilloscope DEMO for a MacBook Pro 13 inch.
# This is the basis for a sound card, almost realtime, AF Oscilloscope in development.
#
# Disclaimer:-
#
# You take this information and use it ENTIRELY at your own risk.
# I hold no responsibility for any errors either in this text or with your electronics capabilities...
#
# The reason I have given this hardware information away is/was because I needed an audio input for
# a simple MacBook Pro Python Audio-Oscilloscope I am developing for the MacBook Pro 13 inch model.
#
# BEST VIEWED IN PLAIN TEXT!
#
# Input/Output adaptor for the Apple MacBook Pro 13 inch only.
# (This MAY be good for the MBP Retina Versions too!)
#
# Mac_OS Version, OSX 10.7.5...
#
# Machine vintage:- August 2012.
#
# Common 3.5mm Mic/Ear socket cable for external MONO audio input, (and stereo audio output)...
#
# Plug required, (or similar)...
#
# http://www.ebay.co.uk/itm/3-5mm-Mini-Jack-Right-Angle-90-Degree-Solder-4-Pole-Male-Plug-Connector-/320770305756
#
# Resistor, 2K2, 1/8W, 10% tolerance...
# Resistor, 33 Ohms, 1W, 10% tolerance, 2 off...
# (Coloured wire as required...)
#
# This is the 4 pole 3.5mm plug wiring, for auto-switching of the Mic input to external...
#
# Pins.               Wiring.
# -----    TIP        -------
#  1 ---->  O  <----- Left Audio Output +ve.
#  2 ---->  H  <----- Right Audio Output +ve.
#  3 ---->  H  <----- Mono (Mic) Input, Active.
#  4 ---->  H  <----- Common To All Inputs And Outputs.
#          ---
#         |   |
#         |   |______
#         |__________|=========
#
# For the microphone auto-switching capability a 2K2 resistor must be connected across Pins 3 and 4, [Mono (Mic) Input, Active and Common]...
# Connect one 33 Ohm resistor between Pins 1 and 4 and the other 33 Ohm resistor between Pins 2 and 4...
#
# Test by plugging into the socket and check that the "System Preferences > Sound" switches over to external input and output.
# Be aware that it takes a few seconds to switch over, it is NOT instantaneous...
#
# You now have two audio outputs at low impedance and an analogue audio input at around 2K2 _impedance_.
#
# Do NOT drive the input with more than 100mV AC and do NOT connect to a DC _supply_ either.
#
# Do NOT load the audio outputs with less than 33 Ohm resistors.
#
# Do NOT assume that Common is connected to GND, Ground, of the computer, although it may well be.
#
# I am assuming that if you are capable of doing this that you are also capable of doing the subtle level tests, etc...
#
# (C)2012, B.Walker, G0LCU. The Cable assembly modifictaions are Public Domain, but the code is GPL2...
#
# Enjoy finding simple solutions to often very difficult problems... ;o)
#
# Tested on Python Versions 2.5.6, 2.6.7 and 2.7.1 with pyaudio installed.
#
# $VER: SimpleScope_OSX.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.

# The imports required...
import os
import sys
import pyaudio

def main():
	# Set everything as global just for this DEMO; my choice... ;o)
	global ScopeScreen
	global ScopeWindow
	global plot
	global position
	global horiz
	global record
	global data
	global grab
	global n
	global dec_val

	# Allocate initial values.
	ScopeScreen="(C)2011, B.Walker, G0LCU."
	ScopeWindow="Simple LF Audio Oscilloscope."
	plot=0
	position=67
	horiz=0
	record=" "
	data=" "
	grab=255
	n=0
	dec_val=0

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
		ScopeWindow=open("ScopeScreen.txt","wb+")
		ScopeWindow.write(ScopeScreen)
		ScopeWindow.close()

		# Access the sound system...
		# A modified version of the pyaudio demo code at:- http://people.csail.mit.edu/hubert/pyaudio/
		stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=48000,input=True,frames_per_buffer=1024)
		all=[]
		for n in range(0,48000/1024*1,1):
			record=stream.read(1024)
			all.append(record)
		stream.close()
		pyaudio.PyAudio().terminate()
		record="".join(all)
		# Convert to unsigned data because paUInt8 does NOT work in Python on a MocBook Pro, 13 inch...
		# "struct.unpack" did not work as predicted so converted longhand; remember, this code is only
		# a proof of concept and may yet be done in 16 bit depth.
		data=""
		for n in range(0,len(record),1):
			dec_val=ord(record[n])
			if dec_val>=0 and dec_val<=127:
				dec_val=dec_val+128
				data=data+chr(dec_val)
			dec_val=ord(record[n])
			if dec_val>=128 and dec_val<=255:
				dec_val=dec_val-128
				data=data+chr(dec_val)

		# Now plot the graph...
		horiz=0
		ScopeWindow=open("ScopeScreen.txt","rb+")
		while horiz<=63:
			# Convert each part of the record string into decimal.
			grab=ord(data[horiz])
			# Now convert to 4 bit depth purely for text mode displays only.
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
		print "Simple Audio Oscilloscope DEMO using pyaudio for OSX 10.7.5."
		print "Ctrl-C to quit..."

main()

# SimpleScope_OSX.py program end; release date:- 07-10-2012...
# Enjoy finding simple solutions to often very difficult problems.
