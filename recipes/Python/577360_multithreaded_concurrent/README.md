## A multithreaded, concurrent version of map()

Originally published: 2010-08-16 22:48:17
Last updated: 2010-08-16 23:04:48
Author: Wai Yip Tung

map() applies a function to a list of data sequentially. This is a variation to map that execute each function call concurrently in a thread.