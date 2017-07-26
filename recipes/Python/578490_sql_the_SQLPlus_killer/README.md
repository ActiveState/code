## sql+ the SQL*Plus killer  
Originally published: 2013-03-12 16:50:30  
Last updated: 2013-03-14 09:13:01  
Author: jo   
  
This recipe is an emulator of the Oracle SQL\*Plus, but it does things in a more friendly way ;).

If you need a client to access your Oracle but you don't like SQL\*Plus, try this one.

This recipe was inspired by James Thiele's Console built with Cmd object recipe.

It provides a 'help' facility and supplies command completion when you hit the 'tab' key.

In addition you can use command line editing and history keys.

Here are the commands that you can use:

    ========================================
    Documented commands (type help <topic>):
    ========================================
    constraints  edit      help     input   sequences  shell
    db           exit      history  output  set        tables
    desc         foreigns  index    quit    settings   triggers


You can edit the queries using 'vim' or any other editor.

The command 'output' can redirect output to a file and command 'input' can input commands from a file.

There's paginated output.

The command 'shell' or '!' allow you to perform operating system commands.

You can add commands by defining methods with names of the form 'do_xxx()' where 'xxx' is
the name of the command you wish to add.

There is a configuration file (.sql+) where you need to enter the dburi, editor name and other
settings.

