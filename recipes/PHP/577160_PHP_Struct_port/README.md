## PHP 'Struct' portOriginally published: 2010-03-28 01:15:24 
Last updated: 2010-03-28 01:22:31 
Author: Jeff Griffiths 
 
In Ruby, the [Struct class](http://ruby-doc.org/core/classes/Struct.html) is a convenient way to create a hash-like object on the fly and use it for your nefarious purposes. PHP 5+ can be convinced to do this type of things as well, it just doesn't have it out of the box. Here is a simple class that implements iterator and allows you to populate the internal data structure similar to how Ruby's Struct works. Syntactic sugar? Probably.\n\nNote: I haven't bothered to implement the Ruby Struct API per se, Instead I just got something similar by implementing the Iterator interface and keeping things very PHP-like.