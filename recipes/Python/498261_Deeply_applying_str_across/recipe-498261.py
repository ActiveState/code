"""Utilities for handling deep str()ingification.

Danny Yoo (dyoo@hkn.eecs.berkeley.edu)


Casual Usage:

    from deepstr import deep_str
    print deep_str(["hello", "world"])


Very unusual usage:

    import deepstr
    import xml.sax.saxutils
    
    def handle_list(obj, deep_str):
        if isinstance(obj, list):
            results = []
            results.append("<list>")
            results.extend(["<item>%s</item>" % deep_str(x)
                            for x in obj])
            results.append("</list>")
            return ''.join(results)

    def handle_int(obj, deep_str):
        if isinstance(obj, int):
            return "<int>%s</int>" % obj

    def handle_string(obj, deep_str):
        if isinstance(obj, str):
            return ("<string>%s</string>" %
                    xml.sax.saxutils.escape(obj))

    def handle_default(obj):
        return "<unknown/>"

    silly = deepstr.DeepStr(handle_default)
    silly.recursive_str = deepstr.make_shallow_recursive_str(
        "<recursion-detected/>")
    silly.register(handle_list)
    silly.register(handle_int)
    silly.register(handle_string)
    print silly([3, 1, "four", [1, "<five>", 9.0]])
    x = []
    x.append(x)
    print silly(x)


This module provides a function called deep_str() that will do a deep
str() on objects.  This module also provides utilities to develop
custom str() functions.


(What's largely undocumented is the fact that this isn't really about
strings, but can be used as a general --- and convoluted --- framework
for mapping some process across data.)

"""

import unittest
    


def make_shallow_recursive_str(recursion_label):
    def f(obj, deep_str):
        return recursion_label
    return f


class DeepStr:
    """Deep stringifier."""
    def __init__(self,
                 default_str=str, 
                 recursive_str=make_shallow_recursive_str("...")):
        """
        DeepStr: stringify_function handler -> stringify_function
        
        Creates a new DeepStr.  Once constructed, you can call as
        if this were a function that takes objects and returns
        strings.

        default_str is the default function used on types that this
        does not recognize.  It must be able to take in an object and
        return a string.

        If we hit structure that's already been traversed,
        we use recursive_str on that structure."""
        self.handlers = []
        self.default_str = default_str
        self.recursive_str = recursive_str


    def __call__(self, obj):
        """Takes an object and returns a string of that object."""
        return self.deepstr(obj, {})


    def deepstr(self, obj, seen):
        ## Notes: this code is a little trickier than I'd like, but
        ## I don't see a good way of simplifying it yet.  Subtle parts
        ## include the construction of substructure_deepstr, and use
        ## of a fresh dictionary in 'new_seen'.
        if id(obj) in seen:
            ## TRICKY CODE: the recursive function is taking in a
            ## stringifier whose 'seen' dictionary is empty.
            def fresh_deepstr(sub_obj):
                return self.deepstr(sub_obj, {})
            return self.recursive_str(obj, fresh_deepstr)

        def substructure_deepstr(sub_obj):
            new_seen = dict(seen)
            new_seen[id(obj)] = True
            return self.deepstr(sub_obj, new_seen)

        for h in self.handlers:
            result = h(obj, substructure_deepstr)
            if result != None:
                return result
        return self.default_str(obj)


    def register(self, handler):
        """register: (object str_function -> string or None)

           Registers a new handler type.  Handers take in the object
           as well as a str() function, and returns either a string if
           it can handle the object, or None otherwise.  The second
           argument should be used on substructures."""
        self.handlers.append(handler)



######################################################################

## Below here is a sample implementation for deep_str()

def handle_list(obj, deep_str):
    if isinstance(obj, list):
        return "[" + ", ".join([deep_str(x) for x in obj]) + "]"
    return None

def handle_tuple(obj, deep_str):
    if isinstance(obj, tuple):
        return "(" + ", ".join([deep_str(x) for x in obj]) + ")"
    return None

def handle_dict(obj, deep_str):
    if isinstance(obj, dict):
        return ("{" + 
                ", ".join([deep_str(k) + ': ' + deep_str(v)
                           for (k, v) in obj.items()]) + 
                "}")
    return None

def handle_recursion(obj, deep_str):
    if isinstance(obj, list): return "[...]"
    ## tuples aren't handled; from my best understanding,
    ## it's not possible to construct a tuple that contains itself.
    if isinstance(obj, dict): return "{...}"
    return "..."

deep_str = DeepStr(str, handle_recursion)
deep_str.register(handle_list)
deep_str.register(handle_tuple)
deep_str.register(handle_dict)



######################################################################
## Sample exercising code.  This is here just to show a wacky example.

def _exercise():
    import xml.sax.saxutils
    def handle_list(obj, deep_str):
        if isinstance(obj, list):
            results = []
            results.append("<list>")
            results.extend(["<item>%s</item>" % deep_str(x)
                            for x in obj])
            results.append("</list>")
            return ''.join(results)

    def handle_int(obj, deep_str):
        if isinstance(obj, int):
            return "<int>%s</int>" % obj

    def handle_string(obj, deep_str):
        if isinstance(obj, str):
            return "<string>%s</string>" % xml.sax.saxutils.escape(obj)

    def handle_default(obj):
        return "<unknown/>"

    silly = DeepStr(handle_default)
    silly.recursive_str = make_shallow_recursive_str(
        "<recursion-detected/>")
    silly.register(handle_list)
    silly.register(handle_int)
    silly.register(handle_string)
    print silly([3, 1, "four", [1, "<five>", 9.0]])
    x = []
    x.append(x)
    print silly(x)


######################################################################

## Test cases
class MyTests(unittest.TestCase):
    def testSimpleThings(self):
        for obj in [42, 'hello', 0+1j, 2.3, u'world']:
            self.assertEquals(str(obj), deep_str(obj))

    def testSimpleLists(self):
        self.assertEquals(str([1, 2, 3]), deep_str([1, 2, 3]))

    def testListsWithStrings(self):
        self.assertEquals("[hello, world]", deep_str(["hello", "world"]))

    def testRepeatedObjects(self):
        self.assertEquals("[1, 1]", deep_str([1, 1]))

    def testRecursion(self):
        L = [1, 2]
        L.append(L)
        self.assertEquals("[1, 2, [...]]", deep_str(L))

    def testSimpleDict(self):
        self.assertEquals("{hello: world}", deep_str({'hello' : 'world'}))

    def testDictWithRecursion(self):
        D = {}
        D[1] = D
        self.assertEquals("{1: {...}}", deep_str(D)) 

    def testNonRecursion(self):
        a = ['a']
        L = [a, a]
        self.assertEquals("[[a], [a]]", deep_str(L))


if __name__ == '__main__':
    unittest.main()
