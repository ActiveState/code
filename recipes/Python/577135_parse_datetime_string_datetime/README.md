## parse a date/time string to a `datetime` instance 
Originally published: 2010-03-21 21:38:48 
Last updated: 2010-04-02 07:32:17 
Author: Trent Mick 
 
    >>> import datetime\n    >>> str(datetime.datetime.now())\n    '2010-03-21 21:33:32.750246'\n    >>> str(datetime.date.today())\n    '2010-03-21'\n\nThis function goes the other way for date and datetime strings of this format.