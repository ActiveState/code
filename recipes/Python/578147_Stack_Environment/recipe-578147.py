#!/usr/bin/env python

"""
stackEnv -- a module providing a stack-based environment to automatically
            transfer some arguments (stackEnv) to called functions without
            passing them explicitly in the call, thus forming a kind of
            hierarchical environment as known from Unix processes
"""

import sys
import unittest

### internals
##############################

_PREFIX = '__STACKENV:'

def _internalName(name):
    "internally used name for the stackEnv variable of the given name"
    return _PREFIX + name

def _internalDelMarker(name):
    """
    internally used name to marker that the stackEnv variable of the
    given name is deleted below this frame
    """
    return _PREFIX + '!' + name

### low level
##############################

def setStackEnv(frame, name, value):
    """
    set the stackEnv variable of the given name to the given value
    in the given frame
    """
    frame.f_locals[_internalName(name)] = value
    delMarker = _internalDelMarker(name)
    if delMarker in frame.f_locals:
        del frame.f_locals[delMarker]

def delStackEnv(frame, name):
    """
    mark the stackEnv variable of the given name as deleted below the
    given frame
    """
    frame.f_locals[_internalDelMarker(name)] = True

class NoSuchStackEnv(Exception):
    """
    Exception stating that the a stackEnv variable for the given name
    does not exist
    """
    pass

def getStackEnv(frame, name):
    """
    return the stackEnv variable value of the given name
    """
    internalName = _internalName(name)
    delMarker = _internalDelMarker(name)
    walker = frame
    while walker:
        if delMarker in walker.f_locals:  # explicitly deleted in this frame?
            raise NoSuchStackEnv(name)
        try:
            return walker.f_locals[internalName]
        except KeyError:  # not in this frame
            walker = walker.f_back
    # not found anywhere in the frames above
    raise NoSuchStackEnv(name)

def yieldAllStackEnvItems(frame):
    "yield all stackEnv variable names and values in use above the given frame"
    found = set([])
    walker = frame
    while walker:
        for name, value in walker.f_locals.iteritems():
            if name.startswith(_PREFIX):
                name = name[len(_PREFIX):]  # strip off prefix
                if name.startswith('!'):  # del marker?
                    found.add(name[1:])  # just store it (w/o '!') as found
                elif name not in found:  # new name?
                    yield name, value
                    found.add(name)
        walker = walker.f_back

### high level
##############################

def setStackEnvs(**kwargs):
    "set a bunch of stackEnv variables in one step via kwargs"
    backFrame = sys._getframe().f_back
    for name, value in kwargs.iteritems():
        setStackEnv(backFrame, name, value)

class StackEnv(dict):
    """
    The singleton instance of this class is the main interface to the stackEnv.
    See the unit test below for example usage (which is as simple as possible).
    """

    def __str__(self):
        return '{ %s }' % ', '.join('%r: %r' % item for item in self.iteritems())

    def __repr__(self):
        return '{ %s }' % ', '.join('%r: %r' % item for item in self.iteritems())

    def iteritems(self):
        return yieldAllStackEnvItems(sys._getframe().f_back)

    def items(self):
        return [ item for item in self.iteritems() ]

    def __iter__(self):
        for name, value in yieldAllStackEnvItems(sys._getframe().f_back):
            yield name

    def __setattr__(self, name, value):
        setStackEnv(sys._getframe().f_back, name, value)

    # TODO: def __iadd__() etc.
    
    def __delattr__(self, name):
        delStackEnv(sys._getframe().f_back, name)
    
    def __getattr__(self, name):
        return getStackEnv(sys._getframe().f_back, name)
    
    def __contains__(self, name):
        try:
            getStackEnv(sys._getframe().f_back, name)
            return True
        except NoSuchStackEnv:
            return False

    def clear(self):
        # collect the names first to prevent changes during iteration:
        names = [ name
            for name, value in yieldAllStackEnvItems(sys._getframe().f_back) ]
        for name in names:
            delStackEnv(sys._getframe().f_back, name)
    
stackEnv = StackEnv()

### Unit tests
###########################################

class Test(unittest.TestCase):
    def runTest(self):

        def b():
            self.assertEqual(42, stackEnv.a)
            self.assertFalse('b' in stackEnv)
            stackEnv.a = 43
            stackEnv.b = 24
            self.assertEqual(43, stackEnv.a)
            self.assertTrue('b' in stackEnv)
            self.assertTrue(24, stackEnv.b)

        def a():
            self.assertTrue(41, stackEnv.a)
            self.assertTrue('b' in stackEnv)
            self.assertEqual(23, stackEnv.b)
            stackEnv.a = 42
            del stackEnv.b
            self.assertEqual(42, stackEnv.a)
            self.assertFalse('b' in stackEnv)
            b()
            self.assertEqual(42, stackEnv.a)
            self.assertFalse('b' in stackEnv)

        for version in ('short', 'long'):
            if version == 'long':
                stackEnv.a = 41
                stackEnv.b = 23
            elif version == 'short':
                setStackEnvs(a=41, b=23)
            self.assertEqual(41, stackEnv.a)
            self.assertTrue('b' in stackEnv)
            self.assertEqual(23, stackEnv.b)
            a()
            self.assertEqual(41, stackEnv.a)
            self.assertTrue('b' in stackEnv)
            self.assertEqual(23, stackEnv.b)
            stackEnv.clear()
            self.assertFalse('a' in stackEnv)
            self.assertFalse('b' in stackEnv)

def main(argv):
    unittest.main(argv=argv)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
