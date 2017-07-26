## A metaclass that hides details of the attribute name when called.

Originally published: 2012-08-30 10:36:37
Last updated: 2012-08-31 09:53:59
Author: Chaobin Tang (唐超斌)

In cases, where getting an attribute will\n    expose to the client code the detail of\n    the very attribute name, which could be changeable\n    over time.\n    This NamedAndCachedAttributeType is intended to\n    hide this detail by mapping the real attribute name\n    to another name that is maintained by the class itself.\n    By doing so, the content provider(this class) and the client\n    code(the caller) establish a deal that the changes of names\n    are taken care of by the provider itself.\n    Second, the value is set as a class variable once it is\n    first retreived, as being cached.