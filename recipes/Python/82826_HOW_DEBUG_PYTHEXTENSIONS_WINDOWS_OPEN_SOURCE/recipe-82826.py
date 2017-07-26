Author: Gerhard Haering (gerhard@bigfoot.de)


0. Scope of this HOWTO
----------------------

This howto describes how to debug *native* win32 Python extensions with open
source tools. See Appendix A for how to do this with Cygwin's Python (which is
much simpler).


1. Prepare Python for development with gcc
------------------------------------------

- Install native Python: http://www.python.org/

- Install Cygwin (you'll need gcc, gdb, ...) http://www.cygwin.com/

- Get the dll2def package from
  http://home.trouwweb.nl/Jerry/packages.html#LIB2DEF unzip and put the
  executable somewhere in your path (it put such stuff in c:\opt\tools)

- Open the Cygwin shell and chdir to the libs directory of your Python
  installation

- Create a python21.def file
    $ dll2def c:/winnt/system32/python21.dll >python21.def
  
  (Adjust the path to the python dll if you use Windows 9x or don't have your
  OS installed in c:/winnt)

- Create a libpython21.a file

    $ dlltool --dllname python21.dll --def python21.def --output-lib \
    libpython21.a

- Create a fake debugging environment for distutils

    (the debugging files download from python.org is of no use, because Cygwin
     gdb cannot understand the debugger symbol format used by Visual C++,
     which is used by the Python crew to build the native win32 Python).

    $ cp libpython21.a libpython21_d.a	

- Steps to make your life easier:
    -- Put the directory of the native Python in your PATH.

    -- Copy the native python.exe to something like ntpython.exe to avoid
       confusion with Cygwin's Python


2. Write the extension module
-----------------------------

Here's a buggy extension module:

/* BEGIN FILE crash.c ***********************************************/
#include "Python.h"

PyObject* crash()
{
    char* s = "test!";
    s[0] = 'T';	/* This is asking for trouble :-) */
    
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef crashMethods[] = {
    {"crash", (PyCFunction)crash, NULL, NULL},
    {NULL, NULL}
};

DL_EXPORT(void) initcrash(void)
{
    PyObject *m;

    m = Py_InitModule("crash", crashMethods);
}

/* END FILE crash.c ************************************************/

And the setup.py file to build it:

###### BEGIN setup.py ###############################################
import sys

from distutils.core import setup
from distutils.extension import Extension

setup (
    name = "crash",

    ext_modules = [Extension(
        name="crash",
        sources = [ "crash.c" ]
        )],
)
###### END setup.py --###############################################


3. Build and debug the extension module
---------------------------------------

$ ntpython setup.py build --compiler=mingw32 --debug
$ cd build/lib.win32-2.1/
$ mv crash_d.pyd crash.pyd     # workaround for distutils
$ gdb ntpython

- Run the application in gdb
- Then:
    Python 2.1.1 (#20, Jul 20 2001, 01:19:29) [MSC 32 bit (Intel)] on win32
    Type "copyright", "credits" or "license" for more information.
    >>> import crash
    >>> crash.crash()

- Gdb will point out where the segmentation fault happened


APPENDIX A
----------

How to debug Python extensions on Cygwin.

- You'll need Cygwin installed (the full development environment, including
  gcc, gdb, python, ...)
- write a setup.py file (see above)
- compile the extension with debugging options:
  $ python setup.py build --debug
- $ cd build/lib.cygwin_nt-5.0-1.3.1-i686-2.1 
- $ gdb python
- Run the application
- "import crash"
- "crash.crash()"


APPENDIX B
----------

Unresolved issues:
- How to set breakpoints in extension modules
