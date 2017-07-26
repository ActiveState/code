## Variant of property() allowing one function to be used for multiple attributes.

Originally published: 2003-06-12 07:43:06
Last updated: 2003-06-12 07:43:06
Author: Raymond Hettinger

Saves the name of the managed attribute and uses the saved name\nin calls to the getter, setter, or destructor.  This allows the\nsame function to be used for more than one managed variable.\n<br>\nUsing property() with more than one variable results in many\nlines of duplicate code for the individual getters, setters,\nand destructors.  This recipe shows how to reuse these functions\nfor multiple variables.  Also, it provides default functions so that\nthe only the interesting functions need to be specified.