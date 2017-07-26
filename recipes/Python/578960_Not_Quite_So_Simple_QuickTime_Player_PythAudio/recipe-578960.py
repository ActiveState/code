# QT_Capture.py
# (C)2014, B.Walker, G0LCU.
# Issued under MIT licence.
#
# A DEMO to show how to capture an audio snippet for use in simple AudioScopes, etc...
# Designed around OSX 10.7.x and greater using a _virgin_ OSX install and requires NO dependences.
# NOTE:- Python 2.7.1 is the default OSX 10.7.x Python install.
#
# Tested on Python 2.5.6 to 3.4.1 and saves to the default '$HOME/Movies' directory\folder\drawer.
# The file is a(n) *.aifc type of file and can easily be converted using the default /usr/bin/afconvert shell command
# to most filetypes, including the *.WAV format used here...
# NOTE:- afplay and afconvert are part of the default install on OSX 10.7.x and can be found inside the /usr/bin folder...
#
# OSX 10.7.5, before running this script start QuickTime Player and from its menu select File -> New Audio Recording.
# From the Audio Recording display select the down pointing arrow and select Maximum Quality. Also select the input
# you want to test with; on this MacBook Pro I used the default internal microphone.
# Now close the Audio Recording window down, there is no need to do a recording. Nothing else is needed to do.
#
# Enjoy finding simple solutions to often very difficult problems.
# Bazza...

import os
import sys

# Create a function to do the task. 
def osxcapture(seconds="2"):
	sys.stdout = open("/tmp/OSXCapture", "w")
	# Generate a simple AppleScript file to launch QuickTime Player _silently_.
	print('''tell application "QuickTime Player"
set sample to (new audio recording)
set visible of front window to false
tell sample
delay 1.5
start''')
	print("delay " + seconds)
	print('''stop
end tell
quit
end tell''')
	# Reset stdout back to the default.
	sys.stdout = sys.__stdout__
	# Now capture the audio as '$HOME/Movies/Audio Recording.aifc'...
	os.system("osascript /tmp/OSXCapture")

# OSX 10.7.x and greater has a default shell audio file converter.
# This DEMO CAN convert an 'aifc' file to an unsigned 8 bit, mono, at the _equivalent_ of 48000Hz sampling speed...
# Use:-  afconvert -f 'WAVE' -c 1 -d UI8@48000 "$HOME/Movies/Audio Recording.aifc" $HOME/Movies/sample.wav
# to change to 8 bit unsigned integer, mono at 48000Hz _sampling_ rate.
# Below is a very, very basic function to convert the file into a more usable CD standard format WAV file...
# It is easy to convert to a .RAW data file from a .WAV file for AudioScope/Audio_Oscilloscope displaying purposes,
# this is a task to solve for yourselves. This is the difficult part... 
def audio_convert():
	sys.stdout = open("/tmp/OSXConvert", "w")
	print('''afconvert -f 'WAVE' -c 2 -d I16@44100 "$HOME/Movies/Audio Recording.aifc" $HOME/Movies/sample.wav''')
	sys.stdout = sys.__stdout__
	# This piece of DEMO code DELETES ALL *.aifc files inside $HOME/Movies drawer\folder\directory so be VERY AWARE!
	os.system("chmod 755 /tmp/OSXConvert; /tmp/OSXConvert; rm $HOME/Movies/*.aifc")

# A basic 5 second test. The file created is '$HOME/Movies/Audio Recording.aifc'...
print("Start the DEMO capture using a _hidden_ Quicktime Player as the source...")
osxcapture("5")
print("Capture done!")

# Now convert to a *.WAV file...
print("Now convert to a CD standard WAVE file.")
audio_convert()
print("Conversion done...")

# A TEST using the OSX 10.7.x default shell command afplay and play the file as a simple listening test...
print("Finally a listening test using the default 'afplay'...")
os.system("afplay $HOME/Movies/sample.wav")
print("End of DEMO program...")
# End of QT_Capture.py DEMO...
