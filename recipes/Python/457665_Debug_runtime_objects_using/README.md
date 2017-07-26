## Debug runtime objects using gc.get_objects()

Originally published: 2005-11-27 08:01:49
Last updated: 2005-11-27 08:01:49
Author: Dirk Holtwick

Since Python 2.2 there is a handy function in the Garbage Collection Module called get_objects(). It gives back a list of all objects that are under control of the Garbeage Collector. This way you can extract informations of your application in runtime.