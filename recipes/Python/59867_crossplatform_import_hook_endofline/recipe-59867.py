# Import hook for end-of-line conversion,
# by David Goodger (dgoodger@bigfoot.com).

# Put in your sitecustomize.py, anywhere on sys.path, and you'll be able to
# import Python modules with any of Unix, Mac, or Windows line endings.

import ihooks, imp, py_compile

class MyHooks(ihooks.Hooks):

    def load_source(self, name, filename, file=None):
        """Compile source files with any line ending."""
        if file:
            file.close()
        py_compile.compile(filename)    # line ending conversion is in here
        cfile = open(filename + (__debug__ and 'c' or 'o'), 'rb')
        try:
            return self.load_compiled(name, filename, cfile)
        finally:
            cfile.close()

class MyModuleLoader(ihooks.ModuleLoader):

    def load_module(self, name, stuff):
        """Special-case package directory imports."""
        file, filename, (suff, mode, type) = stuff
        path = None
        if type == imp.PKG_DIRECTORY:
            stuff = self.find_module_in_dir("__init__", filename, 0)
            file = stuff[0]             # package/__init__.py
            path = [filename]
        try:                            # let superclass handle the rest
            module = ihooks.ModuleLoader.load_module(self, name, stuff)
        finally:
            if file:
                file.close()
        if path:
            module.__path__ = path      # necessary for pkg.module imports
        return module

ihooks.ModuleImporter(MyModuleLoader(MyHooks())).install()
