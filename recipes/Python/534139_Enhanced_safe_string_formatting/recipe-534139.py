import re

# Match any % formatting stanza
# Any character is allowed in names, unicode names work in python 2.2+
# The name can be an empty string
safmt_pat = re.compile(r'''
    %                     # Start with percent,
    (?:\( ([^()]*) \))?   # optional name in parens (do not capture parens),
    [-+ #0]*              # zero or more flags
    (?:\*|[0-9]*)         # optional minimum field width
    (?:\.(?:\*|[0-9]*))?  # optional dot and length modifier
    [EGXcdefgiorsux%]     # type code (or [formatted] percent character)
    ''', re.VERBOSE)

# Wrapper to allow e.g. safmt("%blah", 10, 20, spam='eggs')
# First argument must be the template
def safmt(*args, **kw):
    return safmtb(args[0], args[1:], kw)

# Safe and augmented "%" string interpolation:
# - preserve % stanzas in case of missing argument or key
# - allow mixed positional and named arguments
# Note: TypeError exceptions can still happen, e.g. safmt("%d", "abc")
# Function arguments:
#  template: a string containing "%" format specifiers
#  args    : sequence arguments for format string
#  kw      : mapping arguments for format string
#  savepc  : optionally preserve "escaped percent" stanzas
#            (parameterised positional stanzas always eat args)
#  verb    : verbose execution, prints debug output to stdout
def safmtb(template, args=(), kw=None, savepc=0, verb=0):
    if verb:
        print "safmt(%r)" % (template,)
    
    if kw is None:
        kw = {}
    
    ret = []
    last = i = 0
    d = {}
    di = 0
    pat = safmt_pat
    while 1:
        mo = pat.search(template, i)
        
        if not mo:
            # End of string
            ret.append(template[last:])
            break
        
        i = mo.end(0)
        if verb: print mo.start(), mo.group(0, 1),
        
        stanza, name = mo.group(0, 1)
        if name is not None:
            # str[-1]=='x' is faster than str.endswith('x'),
            # and stanza is always non-empty here so slice will never fail
            if stanza[-1] == "%":
                if savepc:
                    if verb: print 'saving stanza'
                    continue
                # Workaround weird behaviour in python2.1-2.5: a named
                # argument that is just a percent escape still raises
                # KeyError, even though a positional escaped percent eats
                # no args and is happy with an empty sequence.
                # Workaround: provide a dummy key which never gets used.
                dat = stanza % {name: None}
            else:
                try:
                    dat = stanza % kw
                except KeyError:
                    if verb: print 'ignore missing key'
                    continue
            if verb: print "fmt %r" % dat
        else:
            # %<blah>% does not use up arguments, but "%*.*%" does
            numargs = stanza[-1] != "%"
            if verb: print "args=%s" % numargs,
            # Allow for "*" parameterisation (uses up to 2)
            numargs += mo.group(0).count("*")
            if verb: print "args=%s" % numargs,
            
            p = args[di: di + numargs]
            di += numargs
            if verb: print "p=%s" % (p,),
            if len(p) != numargs:
                if verb: print "not enough pos args"
                continue
            if savepc and stanza[-1] == "%":
                if verb: print 'saving stanza'
                continue
            dat = stanza % p
            if verb: print "fmt %r" % dat
        
        ret.append(template[last:mo.start()])
        ret.append(dat)
        last = i
    
    return ''.join(ret)


# ****** Related Recipe ******

from ConfigParser import *
from ConfigParser import DEFAULTSECT
class SafeConfigParser(ConfigParser):
    # Override get() method to use safe string interpolation
    def get(self, section, option, raw=0, vars=None):
        # In python2.3, the name changed from __sections to _sections
        if hasattr(self, '_sections'):
            sections = self._sections
            defaults = self._defaults
        else:
            sections = self._ConfigParser__sections
            defaults = self._ConfigParser__defaults
        
        try:
            sectdict = sections[section].copy()
        except KeyError:
            if section == DEFAULTSECT:
                sectdict = {}
            else:
                raise NoSectionError(section)
        d = defaults.copy()
        d.update(sectdict)
        # Update with the entry specific variables
        if vars:
            d.update(vars)
        option = self.optionxform(option)
        try:
            rawval = d[option]
        except KeyError:
            raise NoOptionError(option, section)

        if raw:
            return rawval

        # do the string interpolation
        value = rawval                  # Make it a pretty variable name
        for depth in range(10):
            oldvalue = value
            value = safmtb(value, kw=d, savepc=1)
            if value == oldvalue: break
        else:
            raise InterpolationDepthError(option, section, rawval)
        
        return value
