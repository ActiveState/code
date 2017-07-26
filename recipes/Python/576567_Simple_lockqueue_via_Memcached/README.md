## Simple lock-queue via Memcached 
Originally published: 2008-11-19 01:32:07 
Last updated: 2008-11-19 01:32:07 
Author: Tal Einat 
 
A simple lock-queue (FIFO) context manager implemented with [Memcached](http://www.danga.com/memcached/).\n\nIn essence this is a normal lock, where the requests to acquire the lock are granted in the order in which they were originally made. Note that requests to acquire the lock are always blocking.