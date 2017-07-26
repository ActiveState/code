# wincapture.py
# (C)2014, B.Walker, G0LCU.
# MIT Licence...
# This is DEMO code only and has no error detetcion except for Python's own.
# Before running ensure you have an input connected to sample from.
# Laptops usually have builtin mics to talk into.
# If you are using an external source set up the external source
# as a _raw_ input source without noise reductions, ambiences, etc...
# This will give you a starter capture source for an audioscope as an example.
# It is not super fast but hey it is FREE!
# This was designed for Windows Vista and 7 and I have no idea if
# Windows 8.x is included...

import os

# Uses SoundRecorder.exe in quiet mode.
# This will generate a file callled SAMPLE.WAV, 16 bit signed integer depth, stereo,
# at 44100 samples per second inside the C:\Windows\Temp\ folder/directory/drawer...
def wincapture(hours="0000", minutes="00", seconds="59"):
	os.system("SoundRecorder.exe /FILE C:\Windows\Temp\SAMPLE.WAV /DURATION " + hours + ":" + minutes + ":" + seconds)

# A simple 2 second test on Python 2.0.1 to 3.3.2...
# IMPORTANT NOTE:- The first second is not quite a second in size, but 0.95 seconds on
# this test machine using an ancient Windows Vista install, so be aware!!!
wincapture("0000", "00", "02")
