'''Document the package search path.

Aquarium uses a rarely used feature of Python packages that allows multiple
physical directories to map to a single package directory.  In this way, 
Aquarium can have its own ``screen`` directory (for instance), and the app can
have its own ``screen`` directory.  Both Aquarium and the app form directory
hierarchies that are separate, but overlaid upon each other.  A path is used to
search the corresponding directory in each hiearchy for a given module.  For
instance, the module reference ``aquarium.navigation.TopNav`` might result in a
search for::

        $PYTHON_LIBS/aquarium/navigation/TopNav.py
        $APP_LIBS/site-packages/navigation/TopNav.py
        $CHEETAH_CACHE/navigation/TopNav.py

The package path must be set once, very early in the life of the application.
Specifically, it must be set before importing, instantiating, and executing
Aquarium or even AquariumProperties (the package path is needed to *find*
AquariumProperties!).  The package path is a Python global.  Because CGI
executes a new copy of Python for every page hit, in CGI, you must set the
package path at the beginning of every page hit.  For other environments, you
normally set the package path at the same time you are initializing other parts
of your application.  The package path is determined by one of the following:

* If the environmental variable ``AQUARIUM_PACKAGE_PATH`` is set to a colon 
  separated set of paths, then it is used::

    # In Bash.
    export AQUARIUM_PACKAGE_PATH=/.../site-packages

* Otherwise, if ``__main__.packagePath`` is set to a tuple of paths, then it is 
  used.  It is common to set ``__main__.packagePath`` in the ``index.py`` of a
  CGI::

    # In Python.
    import __main__
    __main__.packagePath = ("/.../site-packages",)

* Otherwise, an empty tuple is used.  Only Aquarium modules will be accessible.
  This is helpful when using the Python shell to surf documentation.

Unfortunately, all this magic comes at a modest price.  Whenever you create a
new directory that Aquarium doesn't know about (e.g. ``screen/foobar``), you
must create an ``__init__.py`` in that directory that looks like this::

    """Setup the package search path."""
    packageType = "screen/foobar" # <- You must update this part.

    from __main__ import packagePath
    from os import path
    __path__ = map(lambda (x): path.join(x, packageType), packagePath) + \\
        __path__

Concerning the Python shell, as long as you can reach the aquarium package
(all the various ways to play with ``PYTHONPATH`` are out of scope for this
document), you can use the Python shell to read all of the Aquarium
documentation.  To read the documentation for your own application's Aquarium
classes, set the ``AQUARIUM_PACKAGE_PATH`` before starting the shell::

    $ env AQUARIUM_PACKAGE_PATH=demo/seamstress_exchange/site-packages \\
      python
    >>> import aquarium.screen.MessageList
    >>> help(aquarium.screen.MessageList)

'''

__docformat__ = "restructuredtext"

import __main__
import os

import aquarium


if hasattr(__main__, "packagePath"): 
    packagePath = __main__.packagePath = list(__main__.packagePath)
elif os.environ.has_key("AQUARIUM_PACKAGE_PATH"):
    packagePath = __main__.packagePath = \
        os.getenv("AQUARIUM_PACKAGE_PATH").split(":")
else:
    packagePath = __main__.packagePath = []

# If a package foo has an Aquarium-style foo/__init__.py that shadows our
# foo/__init__.py, having Aquarium itself in the packagePath is necessary.

packagePath = __main__.packagePath = \
    packagePath + [os.path.dirname(aquarium.__file__)]

__path__ = packagePath + __path__
