## A white noise generator to sooth baby to sleep.  
Originally published: 2017-05-13 12:12:29  
Last updated: 2017-05-13 12:12:30  
Author: Barry Walker  
  
This is a simple BASH, DASH and SH script to sooth a newborn baby to sleep for a laptop with a builtin mic. Develeoped around an Apple MacBook Pro.\n\nUsage:- [./]shush.sh <time in seconds from 18 to 2700> [sensitivity [Hh|Mm|Ll]]<CR>\n\nIf time is omitted it defaults to 2 bursts of 9 seconds each and if sensitivity is omitted defaults to [M]edium.\n\nIt uses Quicktime Player for Apple OSX 10.12.4 minimum /dev/dsp for CygWin and some Linux flavours and arecored for Linux ALSA machines for baby awake detector.\n\nUpon the two arguments the white noise generator runs for approximately the time given in $1 in bursts of 9 seconds until the time limit is reached.\n$2 is used to detect of baby is awake and reruns the noise generator again with a new noise waveform.\n\nEnjoy...