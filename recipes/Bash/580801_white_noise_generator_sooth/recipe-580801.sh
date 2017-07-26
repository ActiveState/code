#!/bin/sh
# !/usr/local/bin/dash
# shush.sh
# Usage:- [./]shush.sh <time in seconds from 18 to 2700> [sensitivity [Hh|Mm|Ll]]<CR>

: > /tmp/noise.raw
: > /tmp/noise.wav
: > /tmp/wakeupcall.raw
: > /tmp/wakeupcall.wav
: > /tmp/Untitled.m4a

clear

echo ""
echo " A white noise generator to calm baby to sleep."
echo " Public Domain, 2017, (CC0 Licence), for www.unix.com by Barry Walker."
echo ""
echo " It WILL pause after the timer is finished to detect if baby is awake to re-run."
echo ""
echo " Usage:- [./]shush.sh <time in seconds from 18 to 2700> [sensitivity [Hh|Mm|Ll]]"
echo " The default sensitivity in [M] for Medium."
echo ""
echo " For more informaton about this effect:-"
echo " https://en.wikipedia.org/wiki/White_noise_machine "
echo ""
printf " Press Ctrl-C, whilst the noise is sounding, to stop! "

COUNT=1
DECIMAL=0
NAN="Licence CCO, 2017, Barry Walker"
LIMIT=$1
HML=$2
U_NAME=$( uname | awk '{print substr ($0, 0, 5)}' )
HIGH=192
LOW=64
DECIMAL_ARRAY=""

# Error check!
case $LIMIT in
	''|*[!0-9]*)	LIMIT=18 ;;
esac
if [ "$LIMIT" = "" ] || [ "$LIMIT" -le 18 ] || [ "$LIMIT" -ge 2701 ]
then
	LIMIT=18
fi
LIMIT=$(( LIMIT / 9 ))

# Sensitivity level, default is [M]edium and can be omitted.
if [ "$HML" = "H" ] || [ "$HML" = "h" ]
then
	HIGH=144
	LOW=112
fi
if [ "$HML" = "L" ] || [ "$HML" = "l" ]
then
	HIGH=240
	LOW=16
fi

# Use QuickTime Player for OSX 10.12.x, this may FAIL at any time in the future due to OSX _upgrades_.
QuickTime_Player()
{
# Set /tmp/Untitled.m4a file to full R/W capability inside this function.
echo "" > /tmp/Untitled.m4a
chmod 666 /tmp/Untitled.m4a
# This takes about 5 seconds per sample total and is for OSX 10.12.x, (and greater?)...
osascript << AppleSampler
	tell application "QuickTime Player"
		activate
		set savePath to "Macintosh HD:tmp:Untitled.m4a"
		set recording to new audio recording
		set visible of front window to false
		delay 2
		start recording
		delay 2
		stop recording
		export document "Untitled" in file savePath using settings preset "Audio Only"
		close (every document whose name contains "Untitled") saving no
		tell application "System Events" to click menu item "Hide Export Progress" of menu "Window" of menu bar 1 of process "QuickTime Player"
		delay 1
		quit
	end tell
AppleSampler
}

# Listen out for baby crying.
wakeupcall()
{
	printf "0" > /tmp/wakeupcall.raw
	# Use /dev/dsp for GYGWIN.
	if [ "$U_NAME" = "CYGWI" ]
	then
		dd if=/dev/dsp of=/tmp/wakeupcall.raw bs=1 count=12000 > /dev/null 2>&1
		sleep 5
	fi
	# Use QuickTime Player for Darwin. (Working as of OSX 10.12.2.)
	if [ "$U_NAME" = "Darwi" ]
	then
		# This is _SLOW_ but requires NO dependencies.
		QuickTime_Player > /dev/null 2>&1
		afconvert -f 'WAVE' -c 1 -d UI8@8000 /tmp/Untitled.m4a /tmp/wakeupcall.wav
		dd if=/tmp/wakeupcall.wav of=/tmp/wakeupcall.raw skip=4096 bs=1 count=8000 > /dev/null 2>&1
	fi
	# Use either /dev/dsp OR arecord for Linux flavours.
	if [ "$U_NAME" = "Linux" ]
	then
		dd if=/dev/dsp of=/tmp/wakeupcall.raw bs=1 count=12000 > /dev/null 2>&1
		arecord -d 1 -c 1 -f U8 -r 8000 -t raw /tmp/wakeupcall.raw > /dev/null 2>&1
		sleep 5
	fi
	# NOTE: This is NOT an DECIMAL_ARRAY but a space delimited series of decimal integers.
	DECIMAL_ARRAY=$( od -An -tu1 /tmp/wakeupcall.raw )
	for DECIMAL in $DECIMAL_ARRAY
	do
		NAN=""
		if [ "$DECIMAL" -le $LOW ] || [ "$DECIMAL" -ge $HIGH ]
		then
			NAN=$DECIMAL
			sleep 1
			break
		fi
	done
}

# Main loop.
while :
do
	COUNT=1

	# WAV header code for a different noise sound per run.
	printf "%b" "\122\111\106\106\044\000\001\000\127\101\126\105\146\155\164\040\020\000\000\000\001\000\001\000\100\037\000\000\100\037\000\000\001\000\010\000\144\141\164\141\000\000\001\000" > /tmp/noise.wav
	# Create the noise binary.
	dd if=/dev/urandom of=/tmp/noise.raw bs=1 count=65536 > /dev/null 2>&1
	# Generate a RAW and WAV file.
	cat /tmp/noise.raw >> /tmp/noise.wav

	while [ "$COUNT" -le "$LIMIT" ]
	do
		# CygWin /dev/dsp, Linux OSS or PulseAudio.
		> /dev/null 2>&1 cat /tmp/noise.raw > /dev/dsp
		# Linux ALSA.
		aplay /tmp/noise.wav > /dev/null 2>&1
		# Apple OSX 10.12.x and greater.
		afplay /tmp/noise.wav > /dev/null 2>&1
		COUNT=$(( COUNT + 1 ))
	done
	while :
	do
		wakeupcall > /dev/null 2>&1
		if [ "$NAN" != "" ]
		then
			break
		fi
	done
done
