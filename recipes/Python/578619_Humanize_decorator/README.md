## Humanize decorator 
Originally published: 2013-07-31 16:04:13 
Last updated: 2013-07-31 16:04:13 
Author: tomer filiba 
 
When you need to inspect Python objects in a human-readable way, you're usually required to implement a custom ``__str__`` or ``__repr__`` which are just boilerplate (e.g., ``return "Foo(%r, %r, %r)" % (self.bar, self.spam, self.eggs)``. You may implement ``__str__`` and ``__repr__`` by a base-class, but it's hard to call it *inheritance* and moreover, you may wish to remove it when you're done debugging.\n\nThis simple (yet complete) recipe is a class decorator that injects ``__str__`` and ``__repr__`` into the class being printed. It handles nesting and even cycle detection, allowing you to just plug it into existing classes to get them pretty-printed and perhaps remove it later.