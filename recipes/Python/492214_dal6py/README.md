## dal_6.py 
Originally published: 2006-04-26 10:29:40 
Last updated: 2006-09-30 00:29:59 
Author: Stephen Chappell 
 
DAL6 provides the cap of the Disk Abstraction\nLayers and a way to create Context objects.\nThese Context objects provide relative paths\nand keep track of the Currect Working\nDirectory. A method for renaming was\naccidentally left out of the API. This\nrecipe also provides a full abstraction for\nfiles involving full buffering and including\nmost of methods that should be expected.