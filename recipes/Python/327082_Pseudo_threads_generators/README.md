###Pseudo threads with generators and PyGTK/gnome-python

Originally published: 2004-11-05 06:33:06
Last updated: 2004-11-05 06:33:06
Author: Arjan Molenaar

A thread-like interface for those who want to "use" threads in Python with PyGTK. I use it when loading files and display a nice progress bar. The function or method you give to GIdleThread should "yield" every now and then. This makes it simpler to write code, since you do not have to care about nasty locks.