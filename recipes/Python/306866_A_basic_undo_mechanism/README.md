## A basic undo mechanism  
Originally published: 2004-10-02 14:47:56  
Last updated: 2004-10-02 14:47:56  
Author: Bernhard Mulder  
  
Providing undo has become a standard feature for interactive programs. One approach to implement undo is to code each user level operation in three variants: a "do" version, an "undo" version, and a "redo" version.

If you can meet the requirements of this module, you only have to code the "do" variant.

This recipe builds on recipes http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/306864 and http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/306865. It assumes that those recipes are stored as list_dict_observer.py and scalar_observer.py, respectivly.