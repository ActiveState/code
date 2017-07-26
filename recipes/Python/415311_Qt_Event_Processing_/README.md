## Qt Event Processing & Python Threads

Originally published: 2005-05-26 13:17:01
Last updated: 2005-09-10 23:15:15
Author: Jonathan Kolyer

This class forms a bridge between the main Qt event loop and python-based threads.    This was a thorny problem to figure out, so I'm posting for others to benefit.  Basically, you need to invoke all Qt GUI calls and (ActiveX calls on Windows) from the main Qt thread.  But if you're using Python threads, you need to manage the interaction yourself.