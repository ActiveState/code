## Dynamically modifying class attributes at runtime

Originally published: 2011-03-31 20:07:18
Last updated: 2011-03-31 20:07:18
Author: Nabil Stendardo

However considered bad programming, Ruby/JavaScript-like open classes (i.e. classes which can be modified at runtime) actually can be a programming pattern when developing plug-in architectures. And, guess what, Python has that functionality too. This code allows to add attributes (typically methods) to classes, even when already instantiated.