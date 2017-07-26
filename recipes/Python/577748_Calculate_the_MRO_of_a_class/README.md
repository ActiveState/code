## Calculate the MRO of a class 
Originally published: 2011-06-11 08:31:09 
Last updated: 2011-06-11 08:31:09 
Author: Steven D'Aprano 
 
This function allows you to calculate the Method Resolution Order (MRO, or sometimes linearization) of a class or base classes. This is the so-called "C3" algorithm, as used by Python (new-style classes, from version 2.3 and higher). The MRO is the order of base classes that Python uses to search for methods and attributes. For single inheritance, the MRO is obvious and straight-forward and not very exciting, but for multiple inheritance it's not always obvious what the MRO should be.\n\n