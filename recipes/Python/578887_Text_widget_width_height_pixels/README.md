## Text widget width and height in pixels (Tkinter) 
Originally published: 2014-06-06 14:27:27 
Last updated: 2016-12-11 13:39:08 
Author: Miguel Martínez López 
 
The solution consists in putting the Text widget inside a frame, forcing the frame to a fixed size by deactivating size propagation and configuring the Text widget to expand and fill both directions (to stick to the frame borders).\n\nhttps://stackoverflow.com/questions/14887610/how-to-specify-the-dimensions-of-a-tkinter-text-box-in-pixels