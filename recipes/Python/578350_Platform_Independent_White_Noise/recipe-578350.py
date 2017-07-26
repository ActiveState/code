# Noise_Generator.py
#
# A mono "White Noise" generator using STANDARD text mode Python 2.6.x to at least 2.7.3.
# This kids level noise generator is mainly for a MacBook Pro, (13 inch in my case), OSX 10.7.5 and above.
# It is another simple piece of testgear for the young amateur electronics enthusiast and
# uses pyaudio fully installed for it to work. Enjoy... ;o)
# PyAudio can be obtained from here:- http://people.csail.mit.edu/hubert/pyaudio/
#
# Written in such a way that anyone can understand how it works!
#
# It also works on Windows Vista, 32 bit, on various machines with Python 2.6.x to 2.7.3.
# It also works on Debian 6.0.0 using Python 2.6.6 on an HP dv2036ea notebook.
#
# The hardware modifictions can be found here:-
# http://code.activestate.com/recipes/578282-for-macbook_pro-heads-only-simple-lf-audio-oscillo/?in=lang-python
#
# A GPL3 pure sinewave generator can be found here:-
# http://code.activestate.com/recipes/578301-platform-independent-1khz-pure-audio-sinewave-gene/?in=lang-python
#
# Ensure the sound is enabled and the volume is turned up.
#
# Copy the file to a folder/drawer/directory of your choice as "Noise_Generator.py" without the quotes.
#
# Start the Python interpreter from a Terminal/CLI window.
#
# To run the noise generator, (depending upon the platform), just use at the ">>>" prompt:-
#
# >>> execfile("/full/path/to/Noise_Generator.py")<CR>
#
# And away you go...
#
# This code is issued as Public Domain and you may do with it as you please...
#
# Connect an oscilloscope to the earphone socket(s) to see the noise waveform(s) being generated.
#
# $VER: Noise_Generator.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.

# The required imports...
import pyaudio
import random

# Set up a basic user screen...
# This assumes the default 80x24 Terminal window size...
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n$VER: Noise_Generator.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("A DEMO, kids level, simple white noise generator for the MacBook Pro 13 inch.\n")
print("Also works on Windows Vista and Debian Linux from Python 2.6.x to 2.7.x.")
print("Pyaudio IS required for this to work on the platforms quoted...\n")
print("This DEMO lasts for a few seconds only but it is easy to make it continuous.")
print("It is also easily possible to vary the noise BW.\n")
print("Issued as Public Domain, you may do with this code as you please.\n\n\n\n\n\n\n\n\n\n\n")

# Open the stream required, mono mode only...
# Written _longhand_ so that youngsters can understand how it works...
stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=22050,output=True)

# Now generate the _white_noise_ at the speakers/headphone output for a few seconds...
for n in range(0,220000,1): stream.write(chr(int(random.random()*256)))

# Close the open _channel(s)_...
stream.close()
pyaudio.PyAudio().terminate()

# End of Noise_Generator.py program...
# Enjoy finding simple solutions to often very difficult problems... ;o)
