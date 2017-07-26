###Determining the current functions name (at the time it is called)

Originally published: 2003-05-20 15:14:54
Last updated: 2003-05-22 01:30:08
Author: Sean Ross

whoaminow() can be used inside a function to determine, at the time it is called, the name under which that function has been invoked.\n\nNOTE: This solution is *extremely* brittle and provides very limited utility, as it stands. However, it does serve to highlight an interesting avenue for introspection, namely, the dis module.