## Add an entry to a dictionary, unless the entry is already there

Originally published: 2001-08-14 06:10:00
Last updated: 2001-08-14 13:18:30
Author: Alex Martelli

Often, when working with a dictionary D, you need to use the entry D[k] if it's already present, or add a new D[k] if k wasn't a key into D.  The setdefault method of dictionaries is a very handy shortcut for this task.