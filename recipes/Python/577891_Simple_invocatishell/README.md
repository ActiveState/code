## Simple invocation of shell commands  
Originally published: 2011-10-04 23:50:17  
Last updated: 2011-10-21 06:44:35  
Author: Nick Coghlan  
  
Some simple wrappers around the subprocess functions for use in system administration utilities that frequently need to interpolate trusted data into shell commands (e.g. filenames from directory listings, etc):\n\n    import shellcmd\n    return_code = shellcmd.shell_call('ls -l {}', dirname)\n    listing = shellcmd.check_shell_output('ls -l {}', dirname)\n\nEach function invokes the subprocess function of the same name with ``shell=True`` and the supplied command string. Any positional and keyword arguments provided to the call are interpolated into the command string with the ``str.format`` method.