## Auto assign self attributes in __init__ using PEP 484

Originally published: 2017-04-26 17:19:59
Last updated: 2017-04-26 17:26:29
Author: Ryan Gonzalez

TL;DR: Short way of doing stuff like `def __init__(self, a, b): self.a = a; self.b = b`, using type annotations from PEP 484, inspired by Dart's `MyConstructor(this.a, this.b)` and Ruby's/Crystal's/(Moon|Coffee)Script's `constructor/initialize(@a, @b)`.