###Special Range Function for Different Kinds of Ranges (int, float, character)

Originally published: 2011-02-20 01:20:53
Last updated: 2011-03-30 16:42:47
Author: Sunjay Varma

This module allows the user to create a more verbose set of ranges. Simple character ranges, and float ranges are supported.\n\nSupported Ranges:\n* Basic Integer Ranges\n* Float Ranges (as accurate as a float range can get)\n* Simple character ranges (lowercase to lowercase, uppercase to uppercase, etc.)\n\nIt should work in Python 2 and Python 3.\n\n**If you tested this for speed, or want to test this for speed, please post the results! (And your system specs)**\n\n**Edit:** Found a really silly error of mine when using range instead of xrange in these functions!