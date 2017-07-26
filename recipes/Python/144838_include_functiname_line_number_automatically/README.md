## include function name and line number automatically in debug statementsOriginally published: 2002-08-14 15:06:48 
Last updated: 2002-08-14 15:06:48 
Author: Christian Bird 
 
This recipe allows a user to place debug messages, error messages and standard messages throughout a program.  The function name and line number will be added to each debug and error message before it is printed out.  In addition, each of these messages can be passed to multiple handler objects that can direct the output to log files, e-mails, stdout, etc.