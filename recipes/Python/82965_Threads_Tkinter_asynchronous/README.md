## Threads, Tkinter and asynchronous I/O 
Originally published: 2001-10-21 07:14:35 
Last updated: 2001-10-21 07:14:35 
Author: Jacob Hallén 
 
This recipe shows the easiest way of handling access to sockets, serial ports\nand other asynchronous I/O ports while running a Tkinter based GUI.\nIt allows for a worker thread to block in a select(). Whenever something arrives\nit will received and inserted in a queue. The main (GUI) thread then polls\nthe queue 10 times per second (often enough so the user will not notice any\nsignificant delay), and processes all messages that have arrived.\n