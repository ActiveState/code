#!/bin/bash
#
# 1KHz.sh
#
# A very simple DEMO crude sinewave generator using the device /dev/audio in Linux.
# It is an eight second burst and generates an approximation of a pure sinewave using linear interpolation.
# The "sinewave.raw" file length is 65536 bytes in size and saved to your default working directory...
#
# $VER: 1KHz.sh_Version_0.00.10_Public_Domain_2013_B.Walker_G0LCU.

# Zero the raw file...
> sinewave.raw

# This is the binary byte data list for the crude sinewave.
data="\\x0f\\x2d\\x3f\\x2d\\x0f\\x03\\x00\\x03"

# Generate the file as an approximately eight second burst...
for waveform in {0..8191}
do
        printf "$data" >> sinewave.raw
done

# Now play back a single run of the raw data for about eight seconds.
cat sinewave.raw > /dev/audio

# End of 1KHz.sh DEMO...
# Enjoy finding simple solutions to often very simple problems... ;o)
