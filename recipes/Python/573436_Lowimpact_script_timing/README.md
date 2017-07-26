## Low-impact script timing

Originally published: 2008-05-30 12:16:07
Last updated: 2008-07-30 08:43:03
Author: Paul McGuire

As other timing recipes have mentioned, the timeit module could be easier to work with.  Sometimes, I just want to bracket a particular script with start, stop, and duration timing info.  The following module (which I named "timing.py") is about as non-intrusive as you can get - just import the module.