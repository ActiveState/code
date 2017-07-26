###Debugging a running python process by interrupting and providing an interactive prompt

Originally published: 2008-09-25 18:04:58
Last updated: 2008-09-25 11:23:29
Author: Brian McErlean

This provides code to allow any python program which uses it to be interrupted at the current point, and communicated with via a normal python interactive console.  This allows the locals, globals and associated program state to be investigated, as well as calling arbitrary functions and classes.\n\nTo use, a process should import the module, and call listen() at any point during startup.\nTo interrupt this process, the script can be run directly, giving the process Id of the process to debug as the parameter.\n