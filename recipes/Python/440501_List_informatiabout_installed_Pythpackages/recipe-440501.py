#!/usr/bin/env python

# pkgsearch.py - Print information about installed Python packages
# and modules.

import sys, os.path
import compiler
import site

from imp import *

__usage__="""Usage: %s [optional paths] % sys.argv[0])"""

class PkgUtil(object):
    """ Utility class for querying information about
    installed packages and modules """
    
    def __init__(self, paths=None):
        self.paths = sys.path
        if paths:
            self.paths = paths + self.paths

    def find_standard_package(self, pkgname):
        """Search in standard paths for a package/module """

	try:
	    result = find_module(pkgname)
	    return result
        except ImportError, e:
            return ()

    def get_package_init_path(self, pkgname, pkgdir):
        """ Return the init file path for the package.
        This has to be called only for directory packages """

        pkgdir = os.path.abspath(pkgdir)
        
        # Try __init__.py
        pkginitfile = os.path.join(pkgdir, '__init__.py')
        # If it does not exist, try <pkgname>.py
        if not os.path.isfile(pkginitfile):
            pkginitfile = os.path.join(pkgdir,pkgname + '.py')

        if os.path.isfile(pkginitfile):
            return pkginitfile
        else:
            # Everything failed, return pkgdir itself!
            return pkgdir
        
    def load_comments(self, pkgfile):
	""" Open the package and load comments if any. 
	Return the loaded comments """

        # Note: This has to be called with a Python
        # source file (.py) only!
        
	if not os.path.exists(pkgfile):
	    return ""
	
	comment = ""
	
	try:
	    of = open(pkgfile,'rb')
	    data = of.read()
	    if data:
		# Create code object
                try:
                    c = compiler.compile(data,pkgfile,'exec')
                    # Get the position of first line of code
                    if c:
                        lno = c.co_firstlineno
                        lnum = 0
                        # Read file till this line number
                        of.seek(0)
                        for line in of:
                            comment = "".join((comment, line))
                            lnum += 1
                            if lnum==lno or line=="\n": break
                except SyntaxError, e:
                    pass
                except Exception, e:
                    pass
	    of.close()
	except (OSError, IOError, TypeError), e:
            pass
	    
	return comment
	
    def find_package(self, pkgname):
        # Query for package/module and return a dictionary
        # with the following fields
        # 'name': Package/module name,
        # 'path' : Full path of the package/module,
        # 'type' : What kind of a package/module is it
        #          This has the following values
	# 'doc'  : Package documentation
        #
        #          PY_SOURCE: The module was found as a source file. 
        #          PY_COMPILED: The module was found as a compiled code
        #                       object file. 
        #          C_EXTENSION: The module was found as dynamically
        #                       loadable shared library. 
        #          PY_RESOURCE: The module was found as a Macintosh resource.
        #                       This value can only be returned on a Macintosh. 
        #          PKG_DIRECTORY: The module was found as a package directory. 
        #          C_BUILTIN:     The module was found as a built-in module. 
        #          PY_FROZEN:  The module was found as a frozen module.
        #
        # If no module/package is found, returns a null dictionary.
        d = {}
        packages = pkgname.split('.')
        top_level = packages[0]

        try:
            # First look for built-in modules
            result = self.find_standard_package(pkgname)
            if not result and self.paths:
                result = find_module(pkgname, self.paths)
            if result:
                of, pathname, desc = result
                # Last or only component of package
                if len(packages)==1:
		    # Load module
                    try:
                        M = load_module(pkgname, of, pathname, desc)
                    except Exception, e:
                        return d
                    
                    d['name'] = pkgname
                    d['type'] = desc[2]
		    d['doc']=''

                    if os.path.dirname(pathname):
                        d['path'] = self.get_package_init_path(pkgname, pathname)
                    else:
                        # For built-in modules
                        d['path']=pathname
		    if M:
			if M.__doc__:
			    # Set doc string
			    d['doc'] = M.__doc__
			else:
                            pkgfile = ''
			    # Load comments from the package file
			    # if any.
			    if d['type'] == PY_SOURCE:
				pkgfile = d['path']
			    elif d['type'] == PKG_DIRECTORY:
                                if os.path.isfile(d['path']):
                                    pkgfile = d['path']
				
			    if pkgfile:
				d['doc'] = self.load_comments(pkgfile)
			    
                    return d
                
        except ImportError, e:
            if len(packages)>1:
                try:
                    result = find_module(top_level, self.paths)
                    if result:
                        of, pathname, desc = result
                        try:
                            M = load_module(top_level, of, pathname, desc)
                            # Remove the top_level package from the name
                            pkgname = reduce(lambda x,y: x+'.'+y, packages[1:])
                            # Call this recursively
                            if hasattr(M, '__path__'):
                                return self.find_package(pkgname, M.__path__)
                        except ImportError, e:
                            pass
                        except Exception, e:
                            pass
                except ImportError, e:
                    pass

            else:
                pass


        return d

    def pkgTypeInfo(self, pkg_typ):
        """ Return information on the package - Version 2"""

        if pkg_typ is PY_SOURCE:
            return "PYTHON SOURCE FILE MODULES"
        elif pkg_typ is PY_COMPILED:
            return "PYTHON COMPILED CODE OBJECT MODULES "
        elif pkg_typ is C_EXTENSION:
            return "DYNAMICALLY LOADABLE SHARED LIBRARY (C-EXTENSION) MODULES"
        elif pkg_typ is PY_RESOURCE:
            return "MACINTOSH RESOURCE MODULES"
        elif pkg_typ is PKG_DIRECTORY:
            return "PYTHON PACKAGE DIRECTORY MODULES"
        elif pkg_typ is C_BUILTIN:
            return "BUILT-IN MODULES"
        elif pkg_typ is PY_FROZEN:
            return "FROZEN PYTHON MODULES"
        else:
            return "UNKNOWN MODULES"        
    
    def list_packages(self):
        """ An ambitious function which attempts to list all Python packages
        in your system, according to the configuration """

        # First extract loaded module names from sys.modules
        sys_modules = sys.modules.keys()

        packages = {}

        # First add moduels in sys.modules (built-ins,
        # preloads and already loaded ones)
        for name in sys_modules:
            d = self.find_package(name)
            if not d: continue
            try:
                pkginfo = packages[d['type']]
                pkginfo[d['name']] = d['path']
            except Exception, e:
                packages[d['type']] = { d['name'] : d['path'] }

        import site
        # Loop through all directories in sys.path and check for modules
        # Dont iterate through <prefix>/lib directory
        libdir = os.path.join(sys.prefix, 'lib')
        
        walked = []
        for top_level in self.paths:
            if not os.path.isdir(top_level):
                continue

            # Dont iterate through libdir
            if os.path.abspath(top_level) == os.path.abspath(libdir):
                continue
            
            walked.append(top_level)
            for item in os.listdir(top_level):

                fullpath = os.path.join(top_level, item)
                if fullpath in walked: continue

                walked.append(fullpath)
                # Remove the extension
                idx = item.find('.')
                if idx != -1: item = item[:idx]
                d = self.find_package(item)
                if not d: continue
                try:
                    pkginfo = packages[d['type']]
                    pkginfo[d['name']] = d['path']
                except Exception, e:
                    packages[d['type']] = { d['name'] : d['path'] }                
                    
        for key,item in packages.items():
            print
            print self.pkgTypeInfo(key)
            print
            
            # Print sorted
            listofitems = item.keys()
            listofitems.sort()

            for key2 in listofitems:
                print key2,':',item[key2]
        
if __name__=="__main__":
    u = PkgUtil(sys.argv)

    # List information about standard packages
    u.list_packages()

        
