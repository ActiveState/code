###Directory Size (GUI)

Originally published: 2011-02-08 02:15:36
Last updated: 2011-02-09 13:47:54
Author: Stephen Chappell

Have you ever wanted to find out how much room a particular directory was taking up on your hard drive? A roommate of mine in college was having trouble keeping track of where his hard drive space is going, so the following program provided a solution that allows a brief overview of a directory's size along with all of its children. A tree view is created using tkinter and is populated with the directory's name, cumulative size, immediate total file size, and full path. The search button is disabled during a search, and the directory listing with its children is automatically updated.