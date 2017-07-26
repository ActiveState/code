#### The recipe

from __future__ import generators
from inspect import getargspec, formatargspec

_redefinition = """
_redef_tmp = %(name)s
def %(name)s%(oldargs)s:
    wrapped = type('_GeneratorWrapper', (object,), %(name)s._realgen.__dict__)()
    wrapped.__iter__ = lambda self: self
    wrapped.next = %(name)s._realgen%(newargs)s.next
    return wrapped
%(name)s.__doc__ = _redef_tmp.__doc__
%(name)s._realgen = _redef_tmp
del _redef_tmp
"""

def enableAttributes(genfunc):
    """Wrapper for generators to enable classlike attribute access.

    The generator definition should specify 'self' as the first parameter.
    Calls to a wrapped generator should ignore the self parameter.
    """
    old = getargspec(genfunc)
    old[0].pop(0)
    new = getargspec(genfunc)
    new[0][0] = 'wrapped'
    specs = {'name': genfunc.func_name,
	     'oldargs': formatargspec(*old),
	     'newargs': formatargspec(*new)}
    exec(_redefinition % specs, genfunc.func_globals)


#### A minimal, complete example

def outputCaps(self, logfile):
    """Convert to uppercase and emit to stdout and logfile"""
    self.lineno = 1
    while True:
        logfile.write(self.line.upper())
        print self.prefix, self.line.upper(),
        yield None
        self.lineno += 1
outputCaps.prefix = 'Capitalized:'     # Make a class var style default
enableAttributes(outputCaps)           # Wrap the generator in a class

g = outputCaps(open('destfil.txt','w'))
for line in open('sourcefil.txt'):
    g.line = line.rstrip()  # Data can be passed into the generator
    g.next()
    print g.lineno          # Generators can also update the attributes

print dir(g)                # Still has __iter__() and next()
print outputCaps.__doc__    # Docstrings survive wrapping
print g.prefix              # Gen attributes carry through to instances
help(outputCaps)            # PyDoc produces an accurate help screen
