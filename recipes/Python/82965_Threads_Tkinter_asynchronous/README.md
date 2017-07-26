## Threads, Tkinter and asynchronous I/O  
Originally published: 2001-10-21 07:14:35  
Last updated: 2001-10-21 07:14:35  
Author: Jacob Hallén  
  
This recipe shows the easiest way of handling access to sockets, serial ports
and other asynchronous I/O ports while running a Tkinter based GUI.
It allows for a worker thread to block in a select(). Whenever something arrives
it will received and inserted in a queue. The main (GUI) thread then polls
the queue 10 times per second (often enough so the user will not notice any
significant delay), and processes all messages that have arrived.
