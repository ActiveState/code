## File Subclass That Only Returns Additions Since Last Access 
Originally published: 2007-01-22 14:30:24 
Last updated: 2007-01-22 14:30:24 
Author: Ed Gordon 
 
I am writing a log parse script that needs to run ever 10 minutes or so to update some stats in a database. This subclass if the 'file' object looks for a '.filename.pkl' file which contains the seek offset of the previous end of the file, then sets the seek offset to that number before returning the file. On closing the file or StopIteration, it writes the new max offset to this pickle file.