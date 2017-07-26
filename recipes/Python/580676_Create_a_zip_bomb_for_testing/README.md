## Create a zip bomb, for testingOriginally published: 2016-06-07 13:11:49 
Last updated: 2016-06-07 13:11:50 
Author: Simon Harrison 
 
This creates a zip bomb with a programmable recursion depth.  It's useful when you want to create a very deep zip archive for testing decompression software, virus scanners and so on.  Recursion depth is limited by Python itself, so very high values are probably not going to work.  The algorithm could be re-structured to avoid recursion, but I've never needed a nesting depth of more than 900!\n\nEach zip file will get the name stack<n>.zip where <n> is the number of zip files inside each layer.  The data file at the core is called needle.txt.\n\n\n