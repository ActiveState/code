## simple example to show off  itertools.tee

Originally published: 2004-09-23 10:26:53
Last updated: 2004-09-23 22:01:49
Author: John Nielsen

Itertools.tee offers an interesting way to "remember" things that have happened.\nItertools.tee makes multiple iterators from one (if you still have an the original iterator you do not use it). When you advance iterator 1 but not iterator 2, iterator 2 stays behind. Which means, if you later advance iterator 2, it the goes forward through the same data.\n\nIn this example, I use iterator.tee to make 2 iterators, to allow an action to affect data that has been processed in the past. The first iterator, it_main, is what is used to process data normally in this case to do something like display an image selected. The second iterator, it_history, stays behind the first and only advances when a specific action arrives. In effect, it rolls forward through the data that it_main has already processed.