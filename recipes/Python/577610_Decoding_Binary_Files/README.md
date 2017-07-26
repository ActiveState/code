###Decoding Binary Files

Originally published: 2011-03-14 23:59:45
Last updated: 2011-03-15 00:11:10
Author: Yony Kochinski

One way to read files that contain binary fields is to use the `struct` module. However, to do this properly one must learn struct's format characters, which may look especially cryptic when sprinkled around the code. So instead, I use a wrapper object that presents a simple interface as well as type names that are more inline with many [IDLs](http://en.wikipedia.org/wiki/Interface_description_language).