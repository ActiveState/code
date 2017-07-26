## attribute proxy - forwarding attribute access 
Originally published: 2007-03-21 10:28:42 
Last updated: 2007-03-21 10:28:42 
Author: Anders Hammarquist 
 
This recipe lets you transparently forward attribute access to another object in your class. This way, you can expose functionality from some member of your class instance directly, e.g. foo.baz() instead of foo.bar.baz().