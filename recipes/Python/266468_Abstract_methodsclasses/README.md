## Abstract methods/classes

Originally published: 2004-01-23 03:56:01
Last updated: 2004-01-23 23:16:14
Author: Ivo Timmermans

The point is that python doesn't have a notion of abstract methods. Abstract methods are part of an base class that defines an interface, without any code. Abstract methods can't be called directly, because they don't contain any code in their definition.\n\nIn the definition of the base class, you may want to include a specific method that is part of the interface, but the specific implementation is still unknown. A popular example seems to be the drawing of a point or a line in a graphical application.\n\nThe classes Point and Line share several implementation details, but differ on other. In particular, the way they are drawn is completely different (you will want to optimize the drawing of a line). Suppose these two classes are derived from the same class, Object. It is possible to separate the implementation of the method draw of these two classes, while draw can still be called from the base class Object.