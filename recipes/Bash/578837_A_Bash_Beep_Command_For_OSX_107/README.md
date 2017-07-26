## A Bash Beep Command For OSX 10.7+...  
Originally published: 2014-02-27 19:31:28  
Last updated: 2014-02-27 19:36:17  
Author: Barry Walker  
  
This small bash script generates an 8044 byte 1KHz sinewave wave file and immediately plays it.
The file created is a _pure_ sinewave and lasts for 1 second. It uses the default "afplay"
command to run the generated file.

It was designed around an Apple Macbook Pro but using "aplay" it might even work on other *nix
flavours from the command line. I have not bothered to try it as this was purely for my MB Pro.

The wave file can be found as "/tmp/sinewave.wav" during the working session(s) and can be saved
anywhere of your choice.

Enjoy...

(Watch for word wrapping etc...)

Bazza.