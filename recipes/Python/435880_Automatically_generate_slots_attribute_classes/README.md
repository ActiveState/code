## Automatically generate __slots__ attribute for classes and assign attributes on instances  
Originally published: 2005-07-02 11:20:32  
Last updated: 2005-07-02 20:03:32  
Author: Josiah Carlson  
  
There was recently a short discussion about some way to make certain initialization of instances easier (less typing).  This was then followed by an expression of a desire for the automatic generation of the __slots__ attribute for classes (which is generally painful to do by hand for any nontrivial class).  This recipe defines a metaclass and a function.  The 'AutoSlots' metaclass automatically generates a __slots__ attribute during compilation, and the 'InitAttrs' function initializes instance variables during runtime.\n\nA variant which only requires the metaclass would be convenient and would be graciously accepted.