## Dictionary of Function Parameters

Originally published: 2003-05-22 07:33:49
Last updated: 2004-04-28 23:19:59
Author: Sean Ross

This recipe is based on\nhttp://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157572.\n\nCalling parameters() inside a function will return that function's\nparameters as a dictionary. The dictionary does not include *varargs,\nsince *varargs items do not have a "name" that can be used as a key.\nHowever, **varkw is added to the dictionary, as an update.\n\nThere are three optional parameters that can be used to filter the\ninformation returned.