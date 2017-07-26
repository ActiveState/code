###using pyHook to block Windows Keys

Originally published: 2008-04-08 11:24:02
Last updated: 2011-09-18 21:29:17
Author: Brian Davis

Normally you do NOT want to block operating system key combinations but there are a few legitimate cases where you do. In my case I am making a pygame script for my 1 year old to bang on the keyboard and see/hear shapes/color/sounds in response. Brian Fischer on the pygame mailing list pointed me to pyHook. This example was taken from here: http://www.mindtrove.info/articles/pyhook.html and modified to use the pygame event system.