###handler stack

Originally published: 2004-08-28 07:56:16
Last updated: 2004-09-01 18:00:14
Author: Dan Perl

Design pattern that is highly reusable.  Simple handlers implement one specific task from a complex set of tasks to be performed on an object.  Such handlers can then be layered in a stack, in different combinations, together achieving complex processing of an object.  New handlers are easy to implement and add.