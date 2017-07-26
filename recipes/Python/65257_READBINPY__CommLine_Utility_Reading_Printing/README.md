## READBIN.PY -- A Command Line Utility For Reading And Printing A Formatted Hex/Character File Dump

Originally published: 2001-06-21 01:04:24
Last updated: 2001-06-21 01:04:24
Author: Tony Dycks

READBIN is a Text Console-based program which reads a single Input File specified on the command line one character at a time and prints out a formatted hex "dump" representation of the files contents 16 characters per display line.  A prompt for continuation is issued after displaying 20 lines (320 characters of information).  An entry of "X" or "x" followed by the <Enter> key terminates the program execution.  Any other entry followed by <Enter> continues the display of the formatted hex and character information.  A "." character is used for any non-displayable hex character.