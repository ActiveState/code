#!/bin/bash --posix
# beep
# *********************************************************
# Generate a 1 second beep shell command for OSX 10.7.5, default bash terminal.
# Original idea (C)2012, B.Walker, G0LCU.
# Now issued as Public Domain, CC0. You may do with it as you please.
# *********************************************************
> /tmp/sinewave.wav
printf "\x52\x49\x46\x46\x64\x1F\x00\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x40\x1F\x00\x00\x40\x1F\x00\x00\x01\x00\x08\x00\x64\x61\x74\x61\x40\x1F\x00\x00" >> /tmp/sinewave.wav
for n in {0..999}
do
	printf "\x80\x26\x00\x26\x7F\xD9\xFF\xD9" >> /tmp/sinewave.wav
done
# *********************************************************
# The line below uses various Linux flavours, "aplay"...
# aplay /tmp/sinewave.wav
# *********************************************************
# Use the OSX default basic command line audio player, "/usr/bin/afplay".
afplay /tmp/sinewave.wav
# "afinfo" is OSX also...
# afinfo /tmp/sinewave.wav
# *********************************************************
exit 0
# Enjoy finding simple solutions to often very difficult problems...
