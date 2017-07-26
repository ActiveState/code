###Subprocess As Another User

Originally published: 2010-12-10 18:38:26
Last updated: 2010-12-23 00:10:08
Author: Eric Pruitt

Modifies the subprocess module and supplies a new class, LoginSTARTUPINFO, to launch processes as another user on Windows. Requires the pywin32 libraries, but the system ../lib/subprocess.py does not need to be modified.\n\n    >>> import subprocesswin32 as subprocess\n    >>> sysuser = LoginSTARTUPINFO("username", "machine", "passwd123")\n    >>> stdout, stderr = subprocess.Popen("cmd.exe", stdout=subprocess.PIPE,\n    ...     startupinfo=sysuser).communicate()