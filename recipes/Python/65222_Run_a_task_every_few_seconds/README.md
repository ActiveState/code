## Run a task every few seconds 
Originally published: 2001-06-18 04:31:57 
Last updated: 2001-06-18 04:31:57 
Author: Itamar Shtull-Trauring 
 
The TaskThread class allows you to create threads that execute a specific action at a specified interval, by subclassing - just override the task() method. You can also shutdown a TaskThread without having to wait for it to finish "sleeping" (due to the use of threading.Event objects as an alternative to time.sleep()).