## Using a getter for a one-time calculation of a JavaScript object attribute

Originally published: 2010-07-16 18:10:50
Last updated: 2010-07-16 18:10:51
Author: Trent Mick

This is a technique for using a JavaScript getter to calculate the value of an attribute **just the first time**. Rather than caching the value in some private variable and returning it, you just delete the getter and put the calculated value in its place.\n\nNote: I'd read about this technique ages ago, but forgot the details and had to look-up "delete" for removing the getter. :)