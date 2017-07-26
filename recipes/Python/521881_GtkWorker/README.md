## GtkWorker 
Originally published: 2007-06-03 09:06:42 
Last updated: 2007-06-03 09:06:42 
Author: Thomas Ahle 
 
I got inspired to this class, after having read about the java SwingWorker.\nThe problem is that you sometimes have a tough task you want to do in a GUI program, but you don't want the UI to lock.\nThis recipe solves the problem by running the tough code in a background thread, while still letting you do useful interaction with it, like getting the progress or the latest results.