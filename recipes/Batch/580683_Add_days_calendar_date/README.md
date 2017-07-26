###Add days to a calendar date- Julian date

Originally published: 2016-06-16 10:56:40
Last updated: 2016-08-17 10:32:03
Author: Antoni Gual

The trick to add days to a date is to convert the date to a serial, do a normal addition then convert the result back to a date. The serial I use here is the Julian day number used by the astronomers because its conversion formulas arewell documented. If you check the julian day number on internet the result can vary by a day, because julian days  start at noon and i'm not making this distinction. 