## subtract or add a month to a datetime.date or datetime.datetime

Originally published: 2010-06-25 18:41:18
Last updated: 2010-06-25 18:41:19
Author: Trent Mick

Adding or subtracting a month to a Python `datetime.date` or `datetime.datetime` is a little bit of a pain. Here is the code I use for that. These functions return the same datetime type as given. They preserve time of day data (if that is at all important to you).\n\nSee also: \n\n- Recipe 476197: First / Last Day of the Month.\n- [monthdelta module](http://packages.python.org/MonthDelta/)