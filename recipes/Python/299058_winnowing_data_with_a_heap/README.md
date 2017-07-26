###winnowing data with a heap.

Originally published: 2004-08-10 09:02:25
Last updated: 2004-08-11 05:52:17
Author: Douglas Bagnall

The winnow class uses a heap for finding the best few out\nof several items.  At this it is quicker and shorter than\npython 2.3's heapq module, which is aimed at queuing rather\nthan sifting.  OTOH, it is unlikely to have any advantage over\n2.4's heapq, which (I hear) has expanded functionality and is\nimplemented in C.