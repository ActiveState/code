## Logging only new messages while keeping user aware of progressOriginally published: 2005-05-20 05:58:20 
Last updated: 2005-05-20 05:58:20 
Author: Edvard Majakari 
 
Sometimes it is convenient emit a log line only if the log message was different\ncompared to previous message. However, it is also good to log a line at least every n seconds so that user knows the system is working and has not hanged. These\nideas are combined in this very simple recipe.