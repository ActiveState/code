###Using python scripts without .py extension in DOS shells

Originally published: 2006-03-30 07:30:05
Last updated: 2006-03-30 07:30:05
Author: Michael Soulier

One problem with ending all of your python scripts in .py is that you have to type the full name of the command. On Unix you can symlink to it with the shortened name, or wrap it in a bourne-shell script, or a shell alias. None of these solutions is particularly clean.\n\nOn MS Windows, file extensions have much more meaning. In fact, there is an environment variable to control what extensions should be considered executables, to permit them to be run from name, without the extension. This is the PATHEXT environment variable. Add .PY to this, and all of your python scripts can be executed transparently.