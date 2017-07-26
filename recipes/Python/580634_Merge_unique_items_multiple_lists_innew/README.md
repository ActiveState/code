## Merge unique items from multiple lists into a new list  
Originally published: 2016-04-05 18:06:43  
Last updated: 2016-04-05 18:11:49  
Author: Johannes S  
  
Suppose you have multiple lists. You want to print all unique items from the list. Now, what you could do is merge the lists into one_big_list (e.g., a + b +c), and then iterate over each item in one_big_list, etc. The solution proposed here gets this done faster and in one line of code. How? By using **a python set**. A python set is a dictionary that contains only keys (and no values). And dictionary keys are, by definition, unique. Hence, duplicate items are weeded out automatically. Once you have the set, you can easily convert it back into a list. As easy as that!