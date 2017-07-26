#!/usr/bin/env python
"""
True Lieberman-style delegation in Python.

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
"""

__authors__ = ('Alessandro Warth <awarth@cs.ucla.edu>',
               'Martin Blais <blais@furius.ca>',)


class Target(object):

    def __init__(self, n):
        self.n = n

    def send_flowers(self):
        print 'Sending %d flowers from %s' % (self.n, self)

    def fire_missiles(self):
        print 'Firing %d missiles! from %s' % (self.n, self)

    def hang_out(self):
        # Oops! This is not as innocent as it looks!
        print 'Hang out... not so innocently.'
        self.fire_missiles()

t = Target(17)



"""
Given 't', can we make a proxy to it that avoids firing missiles?
"""

import new
from types import MethodType

class Proxy(object):

    def __init__(self, target):
        self._target = target

    def __getattr__(self, aname):
        target = self._target
        f = getattr(target, aname)
        if isinstance(f, MethodType):
            # Rebind the method to the target.
            return new.instancemethod(f.im_func, self, target.__class__)
        else:
            return f



class SafeProxy(Proxy):
    "Override dangerous methods of the target."
    def fire_missiles(self):
        pass

print '--------'
p = SafeProxy(t)
p.send_flowers()
p.hang_out()




class SafeProxy2(Proxy):
    "Override more methods, wrapping two proxies deep."
    def send_flowers(self):
        print 'Sending MORE and MORE flowers: %s' % self.n

print '--------'
p2 = SafeProxy2(p)
p2.send_flowers()
