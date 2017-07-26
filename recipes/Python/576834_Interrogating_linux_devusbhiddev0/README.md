## Interrogating linux /dev/usb/hiddev0 in python  
Originally published: 2009-07-07 01:32:17  
Last updated: 2009-07-07 01:32:17  
Author: Dima Tisnek  
  
What this recipe does:

Maps linux usb hid ioctls and related C structs to python;
Call ioctls, make some sense of output.
Prints all reports for the device with some info.

Works with python 2.4 (tested python 2.4.6 on linux amd64).
Would need changes (e.g. print) for python 3.0.
Might need changes (ioctl signed/unsigned "FIX") for newer python than tested.