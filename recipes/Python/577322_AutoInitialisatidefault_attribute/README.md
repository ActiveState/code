###Auto-Initialisation with default attribute values

Originally published: 2010-07-20 15:00:49
Last updated: 2010-07-20 15:04:52
Author: Luke Dickens

This is a class adapted from one that performs a similar task in the PyML libraries by Asa Ben-Hur et al (see: http://pyml.sourceforge.net/).\n\nThe intention is to speed up development time, by allowing managed attribute names (and their default values) to be specified in a dictionary belonging to each class (here called classinitials). This avoids rewriting the standard initialisation procedure many times over. \n\nSubclasses inherit all superclasses' managed attributes, including the defaults unless overridden. This is found in the property initials. The copy constructor copies all managed attributes.\n\nFinally, any named argument to the __init__ function, whose name appears in the managed attributes dictionary, overrides the class default.\n\nI welcome any comments, criticism or suggested improvements.