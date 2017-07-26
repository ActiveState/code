# sinebeep.py
#
# This creates a file named beep.wav.
#
# (C)2014, B.Walker, G0LCU.
# Issued under the MIT licence.
#
# Works on:-
# The Classic AMIGA A1200, WinUAE and E-UAE from Python 1.4.0 to 2.0.1.
# Windows Vista and 7 from Python 2.0.1 to 3.3.2.
# Linux flavours from Python 2.4.2 to 3.2.2.
# Apple OSX 10.7.5 and above from Python 2.5.6 to 3.4.1.
#
# _Compile_ a 1 second, 1KHz, mono, sinewave burst, ('sinewave.wav'), for general use.
# IMPORTANT!!! This WILL be saved inside the CURRENT drawer/folder/directory so be aware!
def sinebeep():
	header=[ 82, 73, 70, 70, 100, 31, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 16, 0, 0, 0, 1, 0, 1, 0, 64, 31, 0, 0, 64, 31, 0, 0, 1, 0, 8, 0, 100, 97, 116, 97, 64, 31, 0, 0 ]
	waveform=[ 79, 45, 32, 45, 79, 113, 126, 113 ]
	wavefile=open("beep.wav", "w+")
	for hdr in range(0, 44, 1):
		wavefile.write(chr(header[hdr]))
	for sample in range(0, 1000, 1):
		for wf in range(0, 8, 1):
			wavefile.write(chr(waveform[wf]))
	wavefile.close()
# Uncomment the next line to create on on the fly.
# sinebeep()
# Use any standard audio player to hear it...
# For example, the generic 'aplay' for Linux ALSA machines.
