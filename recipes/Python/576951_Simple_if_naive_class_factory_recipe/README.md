###Simple, if naive, class factory recipe in python

Originally published: 2009-11-09 07:58:32
Last updated: 2009-11-09 07:59:53
Author: Ariel Balter

I'm a hack programmer -- no formal education.  So, I don't know if this is technically a "factory", "abstract factory" or something else.\n\nIt is a way to generate a class dynamically, perhaps based on run-time data.\n\nThe point is that you can take a blank class object and dynamically add a constructor, class attributes, and instance methods.  In principle, these could be configured dynamically in a program.\n\nSince I don't know anything about programming theory, I welcome any criticism/discussion/suggestion.  But, please be gentle!\n