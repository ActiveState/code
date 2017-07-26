## Simple command submitter for Win32  
Originally published: 2010-10-25 01:59:47  
Last updated: 2010-10-25 01:59:49  
Author: Phil Rist  
  
This program is a simple Win32 command submitter.  It uses a set of macros similar
to those used by the QEditor program, strings such as '{b}'.  The macros are replaced
with text from a specified file path.  Options to change the working directory and
selected environment variables are provided.  Two examples are provided in the code.  
The program does not collect output or provide input.  It does one call to the expand 
routine.  It can not recognize parameters containing white space.  Do2 which follows
does.  Module is used by Do2 and ButtonBarV1Ex which follow.