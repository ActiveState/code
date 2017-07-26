###safetkinter.py

Originally published: 2012-06-05 02:44:36
Last updated: 2012-06-05 03:23:47
Author: Stephen Chappell

Register tkinter classes with threadbox for immediate usage.\n\nThis module clones several classes from the tkinter library for use with\nthreads. Instances from these new classes should run on whatever thread\nthe root was created on. Child classes inherit the parent's safety.