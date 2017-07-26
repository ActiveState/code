#!/bin/bash --posix
#
# Generate a fun bomb-out sound using SOX and /dev/dsp...
# $VER: bomb.sh_Version_1.00.00_(C)2013_B.Walker_G0LCU.
#
# This is now Public Domain and ypu may do with as you please...
#
# Tested on a Macbook Pro 13" OSX 10.7.5, using SOX.
# Tested on Debian Linux 6.0.x, using /dev/dsp
# Tesetd on PCLinuxOS 2009, using /dev/dsp.
m=0
n=0
waveform="\\xA0\\xA0\\xA0\\x60\\x60\\x60"
# Initialise the waveform.raw file length to zero.
> /tmp/waveform.raw
# Generate the high start sound.
for m in $( seq 0 1 50 )
do
	printf "$waveform" >> /tmp/waveform.raw
done
# Now build up the waveform by adding the correct byte values at the end first then the beginning last.
for n in $( seq 0 1 15 )
do
	# Add the correct byte at the end, append the file, looping a few times...
	waveform="$waveform\\x60"
	for m in $( seq 0 1 10 )
	do
		printf "$waveform" >> /tmp/waveform.raw
	done
	# Now add the correct byte at the beginning, append the file, looping a few times...
	waveform="\\xA0$waveform"
	for m in $( seq 0 1 5 )
	do
		printf "$waveform" >> /tmp/waveform.raw
	done
done
# Now generate a crude explosion...
dd if=/dev/urandom of=/tmp/explosion.raw bs=8000 count=1
# Append to the waveform.raw file...
cat /tmp/explosion.raw >> /tmp/waveform.raw
# Now play back a single run of the raw data using SOX.
# IMPORTANT! Change the path to suit your SOX path...
/Users/barrywalker/Downloads/sox-14.4.0/play -b 8 -r 8000 -e unsigned-integer /tmp/waveform.raw
# A version for /dev/dsp too.
# cat /tmp/waveform.raw > /dev/dsp
#
# DEMO bomb.sh end.
# Enjoy finding simple solutions to often very difficult problems...
