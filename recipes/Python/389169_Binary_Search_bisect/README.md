###Binary Search with the bisect Module

Originally published: 2005-02-22 15:27:36
Last updated: 2005-02-22 15:27:36
Author: Chris Perkins

Writing a binary search algorithm is surprisingly error-prone.  The solution: trick the built-in bisect module into doing it for you.\n\nThe documentation for bisect says that it works on lists, but it really works on anything with a __getitem__ method. You can exploit this fact to make bisect work in ways that you may not have thought of.\n\nExample:  Using a library that controls a digital video camera, I wanted to do a poor-man's auto-exposure.  The goal is to find the exposure time, in milliseconds, that makes the mean pixel value about 128 (out of 0 to 255).\n\nThe trick is to create an object that "looks like" a list to the bisect module.