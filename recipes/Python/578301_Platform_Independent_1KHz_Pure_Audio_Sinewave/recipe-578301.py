# 1KHz_SW_OSX.py
#
# A mono _pure_ sinewave generator using STANDARD text mode Python 2.6.7 to at least 2.7.3.
# This DEMO kids level 1KHz generator is mainly for a MacBook Pro, (13 inch in my case), OSX 10.7.5 and above.
# It is another simple piece of testgear for the young amateur electronics enthusiast and
# uses pyaudio fully installed for it to work. Enjoy... ;o)
# PyAudio can be obtained from here:- http://people.csail.mit.edu/hubert/pyaudio/
#
# It also works on Windows Vista, 32 bit, on various machines with Python 2.6.x to 2.7.3.
# It also works on Debian 6.0.0 using Python 2.6.6 on an HP dv2036ea notebook.
# It also works on "Ubuntu 12.04, Python 2.7, Dell built-in soundcard", with many thanks to Hubert Pham, author
# of pyaudio itself, for testing...
#
# The hardware modifictions can be found here:-
# http://code.activestate.com/recipes/578282-for-macbook_pro-heads-only-simple-lf-audio-oscillo/?in=lang-python
#
# Ensure the sound is enabled and the volume is turned up. Use the volume control to vary the amplitude...
#
# Copy the file to a folder/drawer/directory of your choice as "1KHz_SW_OSX.py" without the quotes.
#
# Start the Python interpreter from a Terminal/CLI window.
#
# To run the sinewave generator, (depending upon the platform), just use at the ">>>" prompt:-
#
# >>> execfile("/full/path/to/1KHz_SW_OSX.py")<CR>
#
# And away you go...
#
# This code is issued as GPL3...
#
# Connect an oscilloscope to the earphone socket(s) to see the sinewave waveform(s) being generated.
#
# $VER: 1KHz_SW_OSX.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.

# The only import required...
import pyaudio

# Initialise the only _variable_ in use...
n=0

# Set up a basic user screen...
# This assumes the minimum default 80x24 Terminal window size...
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n$VER: 1KHz_SW_OSX.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("A DEMO kids level, platform independent, 1KHz _pure_ sinewave generator.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

# Open the stream required, mono mode only...
stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=16000,output=True)

# Now generate the 1KHz signal at the speakers/headphone output for about 10 seconds...
# Sine wave, to 8 bit depth only...
for n in range(0,10000,1): stream.write("\x00\x30\x5a\x76\x7f\x76\x5a\x30\x00\xd0\xa6\x8a\x80\x8a\xa6\xd0")

# Close the open _channel(s)_...
stream.close()
pyaudio.PyAudio().terminate()

# End of 1KHz_SW_OSX.py program...
# Enjoy finding simple solutions to often very difficult problems... ;o)
