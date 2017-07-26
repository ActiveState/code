###Topological Sort

Originally published: 2010-09-28 19:20:30
Last updated: 2010-09-28 19:22:27
Author: Paddy McCarthy

Given items that depend on other items, a topological sort arranges  items in order that no one item precedes an item it depends on.\nIn this example items are strings and dependencies are expressed in a dictionary whose keys are items and whose values are a set of dependent items. Note that the dict may contain self-dependencies (which are ignored), and dependent items that are not also dict keys, such as the item 'ieee'.\n 