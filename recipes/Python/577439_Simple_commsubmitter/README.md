## Simple command submitter for Win32 
Originally published: 2010-10-25 01:59:47 
Last updated: 2010-10-25 01:59:49 
Author: Phil Rist 
 
This program is a simple Win32 command submitter.  It uses a set of macros similar\nto those used by the QEditor program, strings such as '{b}'.  The macros are replaced\nwith text from a specified file path.  Options to change the working directory and\nselected environment variables are provided.  Two examples are provided in the code.  \nThe program does not collect output or provide input.  It does one call to the expand \nroutine.  It can not recognize parameters containing white space.  Do2 which follows\ndoes.  Module is used by Do2 and ButtonBarV1Ex which follow.