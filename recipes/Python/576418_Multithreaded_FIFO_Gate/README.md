## Multithreaded FIFO Gate  
Originally published: 2008-08-13 05:32:48  
Last updated: 2008-09-08 08:29:14  
Author: Anand   
  
While programming with multiple threads, sometimes one needs a construct which allows to suspend the execution of a set of running threads. This is normally required by an outside thread which wants to suspend the running threads for performing a specific action. The threads need to resume after the action in the same order in which they got suspended. 

A thread gate (or gateway) allows you to do this. It acts like a gate through which only one thread can pass at a time. By default the gate is open, allowing all threads to "enter" the gate. When a thread calls "close", the gate is closed, blocking any threads which make a further call to "enter", till the gate is re-opened by the owner, whence the threads resume the order in which they got blocked.

The real-life parallel for this is a human operated level cross, which allows only one vehicle to pass at a time.