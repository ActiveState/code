## A read procedure that allows background event processing  
Originally published: 2001-09-18 15:35:38  
Last updated: 2001-09-18 15:35:38  
Author: Kristoffer Lawson  
  
Sometimes it is useful to be able to read from a channel but not hang
while waiting for data to become available. While this can always be
done with file events (and indeed they are used to implement this) it
is occassionally easier to just read data and let other events handlers
do their business while your "thread" waits for data. Thus bringing us
closer to a thread programming model.