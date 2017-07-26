## An object-oriented enum (Java-like)

Originally published: 2007-06-02 17:24:11
Last updated: 2007-06-02 17:24:11
Author: François Sarradin

Since the version 5, Java includes an enum type in its language. It provides a way to perceive the enumerated types through an object-oriented approach.\n\nIn Java, each enumeration is a particular class and each item of this enumeration is an instance of this class. So, the value of an item can represent an integer, but also a point in a space, a operation, etc. Moreover it is possible to extend an enumeration by using the inheritance.\n\nThis recipe proposes a Python solution to implement the Java enum types, with the help of reflexion.