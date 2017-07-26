###collections.MutableMapping wrapper around _winreg

Originally published: 2010-09-01 12:20:05
Last updated: 2010-09-01 12:20:06
Author: Daniel Stutzbach

The _winreg module is a thin wrapper around the Windows C API to the Windows Registry.  As a thin wrapper, it's not very Pythonic.  This recipe defines a class using the MutableMapping ABC to create a dictionary-like interface to the Windows Registry.