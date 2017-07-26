###Configurable JSON Extensions for Python

Originally published: 2016-05-22 19:00:53
Last updated: 2016-05-22 19:00:54
Author: Michael Blan Palmer

The concept behind the package is to build a single class per type you want to add to json in Python. The new class will have a method for encoding to json and a method for decoding from json. The classes are then loaded into an encoder object and a decoder object that are hooked into the standard json loads\nand dumps functions.