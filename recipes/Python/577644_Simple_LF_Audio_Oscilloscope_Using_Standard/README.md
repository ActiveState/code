## Simple LF Audio Oscilloscope Using Standard Python.  
Originally published: 2011-04-07 17:17:56  
Last updated: 2011-04-07 17:17:57  
Author: Barry Walker  
  
AudioScope.py

I think this might be a first for both Python.

Initially uploaded to LXF, now also here under the MIT licence.

I am building a kids level seismometer and wanted to use standard Python inside Linux.

This DEMO code was my starter idea and looks as though using standard ASCII only might just work a real treat.

I've issued it to LXF under the MIT licence for future reasons.

It doesn't look much on screen except that the waveform(s) shown is/are a basic visual, electrical representation
of your voice. ;o)

It is possible to link the earphone socket on this notebook to the mic input and start the Audio Function
Generator, elsewhere in this site, in a separate Python terminal and see those waveforms inside the
AudioScope.py`s own Python terminal.

This grabs a 1 second 8KB burst, and then displays it onto the Python terminal. The timebase, amplitude, trigger,
single shot and others are not included but the main grab and display using /dev/dsp is shown. This can be made
platform independent by changing the /dev/dsp to something external like the Arduino Dev Board. This uses
STANDARD Python 2.5.x and later and tested on PCLinuxOS 2009 and Debian 6.0.0.

Enjoy finding simple solutions to often very difficult problems.

Bazza, G0LCU.