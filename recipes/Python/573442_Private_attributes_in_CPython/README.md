###Private attributes in CPython

Originally published: 2008-06-05 04:40:14
Last updated: 2008-06-05 04:40:14
Author: Carl Banks

Metaclass that allows for private attributes.  Classes can ensure privacy of their data by checking the stack frame inside __setattr__ and __getattribute__ to see if the function requesting the attribute was defined as part of the class.