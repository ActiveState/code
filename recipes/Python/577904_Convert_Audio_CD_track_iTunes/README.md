## Convert Audio CD track in iTunes with Python 
Originally published: 2011-10-12 05:29:29 
Last updated: 2011-10-12 05:29:30 
Author: Kai Xia 
 
This script would do convert tracks from an audio cd into Apple lossless music using iTunes.\n\nWhen we have a bad cd rom or a bad disk, conversion would usually fail and iTunes would not complain about it. I usually have to check every converted track manually. This script would save the pain: it would check every converted track, if the duration of the converted track is less than the original track, the script would retry the conversion.\n\nThis script is inspired by [Fabien C.](http://code.activestate.com/recipes/users/4010550/) 's Recipe 498241.