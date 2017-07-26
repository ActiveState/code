#!/user/bin/env python 

"""null.py

This is a sample implementation of the 'Null Object' design pattern.

Roughly, the goal with Null objects is to provide an 'intelligent'
replacement for the often used primitive data type None in Python or
Null (or Null pointers) in other languages. These are used for many
purposes including the important case where one member of some group 
of otherwise similar elements is special for whatever reason. Most 
often this results in conditional statements to distinguish between
ordinary elements and the primitive Null value.

Among the advantages of using Null objects are the following:

  - Superfluous conditional statements can be avoided 
    by providing a first class object alternative for 
    the primitive value None.

  - Code readability is improved.

  - Null objects can act as a placeholder for objects 
    with behaviour that is not yet implemented.

  - Null objects can be replaced for any other class.

  - Null objects are very predictable at what they do.

To cope with the disadvantage of creating large numbers of passive 
objects that do nothing but occupy memory space Null objects are 
often combined with the Singleton pattern.

For more information use any internet search engine and look for 
combinations of these words: Null, object, design and pattern.

Dinu C. Gherman,
August 2001
"""

class Null:
    """A class for implementing Null objects.

    This class ignores all parameters passed when constructing or 
    calling instances and traps all attribute and method requests. 
    Instances of it always (and reliably) do 'nothing'.

    The code might benefit from implementing some further special 
    Python methods depending on the context in which its instances 
    are used. Especially when comparing and coercing Null objects
    the respective methods' implementation will depend very much
    on the environment and, hence, these special methods are not
    provided here.
    """

    # object constructing
    
    def __init__(self, *args, **kwargs):
        "Ignore parameters."
        return None

    # object calling

    def __call__(self, *args, **kwargs):
        "Ignore method calls."
        return self

    # attribute handling

    def __getattr__(self, mname):
        "Ignore attribute requests."
        return self

    def __setattr__(self, name, value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, name):
        "Ignore deleting attributes."
        return self

    # misc.

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"


def test():
    "Perform some decent tests, or rather: demos."

    # constructing and calling

    n = Null()
    n = Null('value')
    n = Null('value', param='value')

    n()
    n('value')
    n('value', param='value')

    # attribute handling

    n.attr1
    n.attr1.attr2
    n.method1()
    n.method1().method2()
    n.method('value')
    n.method(param='value')
    n.method('value', param='value')
    n.attr1.method1()
    n.method1().attr1

    n.attr1 = 'value'
    n.attr1.attr2 = 'value'

    del n.attr1
    del n.attr1.attr2.attr3

    # representation and conversion to a string
    
    assert repr(n) == '<Null>'
    assert str(n) == 'Null'


if __name__ == '__main__':
    test()
