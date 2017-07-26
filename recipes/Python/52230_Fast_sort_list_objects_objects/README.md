###Fast sort the list of objects by object's attribute

Originally published: 2001-03-11 07:57:45
Last updated: 2001-03-11 07:57:45
Author: Yakov Markovitch

Fast sorting the list of objects by object's attribute using the "Schwartzian transform". Since this recipe uses _only_ builtins and doesn't use explicit looping, this is quite fast. Besides, it doesn't use any Python 2.0-specific features (such as zip() or list comprehensions) so can be used for Python 1.5.2/1.6 as well.