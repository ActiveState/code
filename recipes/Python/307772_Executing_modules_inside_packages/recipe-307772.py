"""Run a module as if it were a file

Allows Python scripts to be located and run using the Python module namespace
instead of the native filesystem.
"""
from imp import find_module, PY_SOURCE, PY_COMPILED
import sys

__all__ = ['execmodule']

class _ExecError(ValueError): pass

def execmodule(module_name, globals=None, locals=None, set_argv0 = False):
    """Locate the requested module and run it using execfile

    Any containing packages will be imported before the module is executed.
    Globals and locals arguments are as documented for execfile
    set_argv0 means that sys.argv[0] will be set to the module's filename prior
    to execution (some scripts use argv[0] to determine their location).
    """
    if globals is None:
        globals = sys._getframe(1).f_globals # Mimic execfile behaviour
    if locals is None:
        locals = globals
    pkg_name = None
    path = None
    split_module = module_name.rsplit('.', 1)
    if len(split_module) == 2:
        module_name = split_module[1]
        pkg_name = split_module[0]
    try:
        # Import the containing package
        if pkg_name:
            pkg = __import__(pkg_name)
            for sub_pkg in pkg_name.split('.')[1:]:
                pkg = getattr(pkg, sub_pkg)
            path = pkg.__path__
        # Locate the module
        module_info = find_module(module_name, path)
    except ImportError, e:
        raise _ExecError(str(e))
    # Check that all is good
    module = module_info[0]
    filename = module_info[1]
    filetype = module_info[2][2]
    if module: module.close() # We don't actually want the file handle
    if filetype not in (PY_SOURCE, PY_COMPILED):
        raise _ExecError("%s is not usable as a script\n  (File: %s)" %
                          (module_name, filename))
    # Let's do it
    if set_argv0:
        sys.argv[0] = filename
    execfile(filename, globals, locals)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >> sys.stderr, "No module specified for execution"
    del sys.argv[0] # Make the requested module sys.argv[0]
    try:
        execmodule(sys.argv[0], set_argv0 = True)
    except _ExecError, e:
        print >> sys.stderr, e
