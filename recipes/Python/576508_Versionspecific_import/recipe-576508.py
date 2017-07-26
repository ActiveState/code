# In tools/, make a subdirectory _stable_1_0_2 containing the 1.0.2 stable 
# version of the "tools" package.  Make _stable_1_0 and _stable_1 symlinks to that directory,
# assuming you don't have any newer 1.0.x or 1.x releases. Also make a _latest_1_0_2 containing
# the latest (possibly unstable) 1.0.2.x version, and symlink _latest_1_0 and _latest_1 to it.
# Finally, create a _exact_1_0_2_4 if you have, for example, a 1.0.2.4 release of "tools".
#
# Each of those subdirectories is a package that can be loaded as "tools" by the client.



# File: tools/__init__.py

if '_original__import__' not in locals():
    _original__import__ = __import__

def myimport(name, theglobals=None, thelocals=None, fromlist=None, level=-1):
    if name.split('.')[0] != "tools":
        return _original__import__(name, theglobals, thelocals,
                fromlist, level)

    if not currentversion:
        raise Exception("After importing tools, you must "
                "load a specific version by typing something like "
                "'tools = tools.loadstable(\"0.1\")' .")

    def withversion(name):
        """
        Turn "tools[.anything]" into "<versionname>[.anything]" , where
        <versionname> is something like 'tools._stable_0_1' .
        """
        parts = name.split('.')
        parts[0] = currentversion.__name__ # eg 'tools._stable_0_1'
        return '.'.join(parts)

    # "import tools[.whatever.whatever]"
    if not fromlist:
        # use <versionname> instead of "tools", but otherwise execute the 
        # import as expected
        _original__import__(withversion(name), theglobals, thelocals,
                fromlist, level)
        # but return <currentversion> as the top-level package instead of
        # returning tools as expected
        return currentversion

    # "from tools[.whatever.whatever] import thing": instead,
    # "from <versionname>[.whatever.whatever] import thing", and 
    # return thing as expected
    return _original__import__(withversion(name), theglobals, thelocals,
            fromlist, level)
__builtins__["__import__"] = myimport

def loadstable(ver):
    return _loadversion(ver, prefix="_stable_")

def loadunstable(ver):
    return _loadversion(ver, prefix="_latest_")

def loadexact(ver):
    return _loadversion(ver, prefix="_exact_")

def _loadversion(ver, prefix):
    targetname = prefix + ver.replace('.', '_')
    mainpackage = _original__import__("tools", globals(), locals(),
        [targetname])
    global currentversion
    currentversion = getattr(mainpackage, targetname)

    # Let users change versions after choosing this one
    currentversion.loadstable = loadstable
    currentversion.loadunstable = loadunstable
    currentversion.loadexact = loadexact

    return currentversion

currentversion = None




# In the user's code:

# This line makes "tools" be the stable 1.0.2 release.
import tools; tools = tools.loadstable('1')

# Now the user can work with tools as normal
from tools import foo
import tools.bar.bim
from tools.baz import bonk
