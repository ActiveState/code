## Interrogating linux /dev/usb/hiddev0 in python

Originally published: 2009-07-07 01:32:17
Last updated: 2009-07-07 01:32:17
Author: Dima Tisnek

What this recipe does:\n\nMaps linux usb hid ioctls and related C structs to python;\nCall ioctls, make some sense of output.\nPrints all reports for the device with some info.\n\nWorks with python 2.4 (tested python 2.4.6 on linux amd64).\nWould need changes (e.g. print) for python 3.0.\nMight need changes (ioctl signed/unsigned "FIX") for newer python than tested.