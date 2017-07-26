## Saving backups when writing files  
Originally published: 2001-03-26 10:58:04  
Last updated: 2001-05-08 23:12:33  
Author: Mitch Chapman  
  
Before overwriting an existing file it's often desirable to make a backup.  This recipe emulates the behavior of Emacs by saving versioned backups.  It's also compatible with the marshal module, so you can save versioned output in "marshal" format.