## Cross-site scripting (XSS) defense 
Originally published: 2006-08-05 10:45:10 
Last updated: 2006-08-05 10:45:10 
Author: Josh Goldfoot 
 
This cleanses user input of potentially dangerous HTML or scripting code that can be used to launch "cross-site scripting" ("XSS") attacks, or run other harmful or annoying code.  You want to run this on any user-entered text that will be saved and retransmitted to other users of your web site.  This uses only standard Python libraries.