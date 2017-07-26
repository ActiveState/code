## True Lieberman-style delegation in Python.  
Originally published: 2007-05-14 11:14:33  
Last updated: 2007-05-14 11:14:33  
Author: Martin Blais  
  
Proxies are usually implemented as objects that forward method calls to a
"target" object. This approach has a major problem: forwarding makes the target
object the receiver of the method call; this means that calls originating from
the body of a method in the target will not go through the proxy (and thus their
behavior cannot be modified by the proxy).

For example, suppose we want a proxy to an instance of Target (shown below)
that is "safe", i.e., does not do anything bad like firing missiles. We can
just define a class that forwards calls to the safe methods, namely
send_flowers() and hang_out(). This class can have its own version of
fire_missiles() that does nothing. Now consider what happens when we call
the proxy object's innocent-looking hang_out() method. The call is forwarded
to the target object, which in turn calls the target object's (not the
proxy's) fire_missiles() method, and BOOM! (The proxy's version of
fire_missiles() is not called because forwarding has made the target object
the receiver of the new method call.)

By using delegation, one can implement proxies without the drawbacks of the
method-forwarding approach. This recipe shows how Python's __getattr__
method can be used to implement the kind of delegation present in
prototype-based languages like Self and Javascript, and how delegation can
be used to implement better proxies.