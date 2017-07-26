## Builtin i18n _() function in a multi-threaded environment.Originally published: 2006-01-02 10:57:10 
Last updated: 2006-01-02 10:57:10 
Author: Martin Blais 
 
Injecting _() in the __builtin__ module in order to inject global functions _() and N_() is common in applications which need i18n.  This is a variation on the theme that does this in a multi-threaded environment, using threading.local from Python-2.4.