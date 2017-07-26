###imapmethod and friends

Originally published: 2003-10-31 08:03:07
Last updated: 2003-10-31 08:03:07
Author: Michael Hoffman

Ever been frustrated at having to separately read data and then do minor processing by calling methods on the data? Find yourself writing lambda functions or short generators to do intermediate processing between iterators? If so, you can simplify your programming life by using imapmethod instead. Imapmethod calls a named method on each item it iterates through. For example, you can replace [x.rstrip() for x in iterable], which inefficiently generates the whole list at once before processing begins, or the more efficient imap(lambda&nbsp;x:&nbsp;x.rstrip(),&nbsp;iterable) with imapmethod("rstrip",&nbsp;iterable) or even the provided irstrip(iterable).\n\nThis recipe also illustrates some more brain-twisting uses of itertools.