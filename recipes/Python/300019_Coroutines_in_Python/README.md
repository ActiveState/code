## Coroutines in Python 
Originally published: 2004-08-17 08:17:46 
Last updated: 2004-08-23 06:47:19 
Author: Bernhard Mulder 
 
This recipe shows how you can emulate coroutines in pure Python using generators.\n\nWith coroutine I mean a construct as available, for example, in Simula 67 or Modula2. They are like threads with two additional restrictions: at most one coroutine can be running at any time, and each coroutine yields control only at very specific points. Other terms I have heard for this concept are "cooperative multitasking", "non-preemptive multitasking" or Fibers (on Windows).