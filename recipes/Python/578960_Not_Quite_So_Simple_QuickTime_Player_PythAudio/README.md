## Not Quite So Simple QuickTime Player, Python Audio Capture.  
Originally published: 2014-11-08 19:10:57  
Last updated: 2014-11-08 19:10:58  
Author: Barry Walker  
  
Not Quite So Simple QuickTime Player, Python Audio Capture.

This DEMO code captures a function to generate a user 5 second Audio sample in Apple *.aifc format.
It is then converted to DC quailty *.WAV format.

It uses default shell system files to do the task.

An AppleScript is created to do the sample but due to the limitations of QT Player there is a 1.5 second delay to allow QuickTine Player to start up.
It is not entirely quiet but unobtrusive enough as to be like quiet mode...

This is again a means a signal capture for an AudioScope without the need for special tools or installs.

Read the code for more information.

IMPORTANT!!! This DEMO WILL delete all *.aifc files inside the default $HOME/Movies directory, so be aware.

A simple ALSA one is on its way too...

It actually works on Python 3.4.1 but I have no idea if it works below Python 2.5.6...

Bazza...
