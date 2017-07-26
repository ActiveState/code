# RF_Attenuator.py
#
# Another kids level building and coding project...
#
# This DEMO is to show how to generate a simple identical waveform out of each channel
# BUT in anti-phase. A high quality dual trace Oscilloscope will show the waveforms generated 
# are in anti-phase. This simple project uses this technique to produce a _large_ AC
# Voltage across the two _hot_ output sections of the earphone socket. The output from the
# earphone socket is effectively being used in "Bridge Output" mode for this project.
# The circuit below uses this "Bridge Output" technique as a control for this RF Attenuator.
# Originally designed for a Macbook Pro, OSX 10.7.5 and Python 2.6.7 and 2.7.1.
#
# Circuit Diagram.                      +-------+------+----------------------------+
#          Tip --> O <-------------+ AC |       |      |                            |
#  Middle Ring --> H <----+       / \   |       |      |                            \
#  Ground Ring --> H      |      /   \  |       |      |                            /
#                .===.    |     / D1  \ |       |      |                            \
#      Plastic   |   |    |    / |\ |+ \|       |      |                         R2 /
#       Body --> |   |    | - + -| >|-  + +     |      |                            \
#   3.2mm Stereo |   |    |   |\ |/ |  /|       |      |                            /
#    Jack Plug    \ /     |   | \     / |       |      \    J2    || C3     +| /|   |   |\ |+     C4 ||   J3
#        J1        H      |   |  \   /  |  C2 -----    /     O----||----+----|< |---+---| >|----+----||----O
#                 ~~~     |   |   \ /   |     -----    \    I/P   ||    |    | \|       |/ |    |    ||   O/P TO RX
#                         +----)---+ AC |       |   R4 /     O          \     D2         D3     \          O
#                             |     + =====     |      \     |          /                       /          |
#                             |    C1 -----     |      /     |          \                       \          |
#                             |         |       |      |     |       R1 /                    R3 /          |
#                             |         |       |      |     |          \                       \          |
#                             |         |       |      |     |          /                       /          |
#                             |         |       |      |     |          |                       |          |
#                             +---------+-------+------+-----+----------+-----------------------+----------+
#                           __|__
#                           /////
# R1, R2, R3.......................  150 Ohms, 1/4W, 10% tolerance.
# R4...............................  100 KilOhms, 1/4W, 10% tolerance.
# C1...............................  100uf, 16V, electrolytic.
# C2...............................  0.1uf, any type.
# C3, C4...........................  0.01uF, any type.
# D1...............................  Any small bridge rectifier.
# D2, D3...........................  1N4148, small signal diode.
# J1...............................  3.2mm standard stereo jack plug.
# J2, J3...........................  Any reasonable quality RF sockets.
# Enamelled copper wire............  As required.
# Coloured hook up wire............  As required.
# Stripboard.......................  As required.
# NOTE:- This circuit CAN be made simpler by omitting D3 and R3 and connecting C4 to the Anode of D2.
# As a final addendum for the circuit, transformer coupling would completely isolate the computer from the attenuator.
#
# PyAudio can be obtained from here:- http://people.csail.mit.edu/hubert/pyaudio/
# There are various versions for _all_ versions of Python.
#
# Tested on:-
# 1) A Macbook Pro, OSX 10.7.5 and Python 2.6.7 and 2.7.1.
# 2) Windows Vista, 32 bit, on various machines with Python 2.6.x.
# 3) Debian 6.0.0 using Python 2.6.6 on an HP dv2036ea notebook.
#
# Ensure the sound is enabled and the volume is turned up. Use the system volume control to vary the output...
#
# Copy the file to a folder/drawer/directory of your choice as "RF_Attenuator.py" without the quotes.
#
# Start the Python interpreter from a Terminal/CLI window.
#
# To run the RF Attenuetor, (depending upon the platform), just use at the ">>>" prompt:-
#
# >>> exec(open("/full/path/to/RF_Attenuator.py").read())<CR>
#
# And away you go...
#
# This code is issued as Public Domain...
#
# Connect an RF signal generator to the attenuator input. Connect a high quality receiver with a reasonably
# calibrated S-Meter to the attenuator output, both on the same frequency. Vary the output level using the
# OS's global output control and watch the S-Meter vary in unison... There WILL be some insertion loss!
#
# $VER: RF_Attenuator.py_Version_0.00.10_(C)2012-2013_B.Walker_G0LCU.

# The simple code proper...
import pyaudio

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n$VER: RF_Attenuator.py_Version_0.00.10_(C)2012-2013_B.Walker_G0LCU.\n")
print("A DEMO showing how to generate the same waveform in anti-phase for")
print("a kids level, platform independant, SW listener, RF Attenuator...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

# Open the stream required, stereo mode, 8 bit depth per channel...
stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=2,rate=16000,output=True)

# Now generate a signal, 8 bit depth, in anti-phase at the speakers or headphone output socket for about 25 seconds.
# Bytes 1, 3, 5 and 7 are used for the left channel and 2, 4, 6 and 8 for the right channel.
for n in range(0,100000,1): stream.write(b"\x7F\x80\x7F\x80\x80\x7F\x80\x7F")
# This would be the byte string for both waveforms to be in-phase; b"\x7F\x7F\x7F\x7F\x80\x80\x80\x80"

# Close the open _channels_...
stream.close()
pyaudio.PyAudio().terminate()

# End of RF_Attenuator.py program...
# Enjoy finding simple solutions to often very difficult problems... ;o)
