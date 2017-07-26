## A metaclass that hides details of the attribute name when called.  
Originally published: 2012-08-30 10:36:37  
Last updated: 2012-08-31 09:53:59  
Author: Chaobin Tang (唐超斌)  
  
In cases, where getting an attribute will
    expose to the client code the detail of
    the very attribute name, which could be changeable
    over time.
    This NamedAndCachedAttributeType is intended to
    hide this detail by mapping the real attribute name
    to another name that is maintained by the class itself.
    By doing so, the content provider(this class) and the client
    code(the caller) establish a deal that the changes of names
    are taken care of by the provider itself.
    Second, the value is set as a class variable once it is
    first retreived, as being cached.