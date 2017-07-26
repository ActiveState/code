## A simple enum type  
Originally published: 2013-02-13 06:35:24  
Last updated: 2013-02-13 06:53:38  
Author: Eric Snow  
  
Inspired by various threads[1] on the python-ideas list, here's a simple enum type.  Enums are generated either via the class syntax or via Enum.make().

    class Breakfast(Enum):
        SPAM, HAM, EGGS
        BACON, SAUSAGE

    Breakfast = Enum.make("SPAM HAM EGGS BACON SAUSAGE")

Here are some of the features:

Enum:
* inheriting from an enum inherits copies of its values.
* the export() method allows for exposing an enum's values in another namespace.

Enum Values:
* the underlying values within an enum are essentially useless, diminishing the temptation to rely on them.
* identity is equality, like with None, True, and False.
* enum values support bitwise operations within the same enum.
* the result of a bitwise operation is always the same object given the same inputs.

[1] see http://mail.python.org/pipermail/python-ideas/2013-January/019003.html