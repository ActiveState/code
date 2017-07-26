###Get a posix timestamp from a type 1 uuid

Originally published: 2008-08-13 18:56:28
Last updated: 2008-08-13 18:56:29
Author: Kent Tenney

The uuid timestamp is 60 bits, the number of 100 nanosecond increments since Oct. 15, 1582\nThis simple function returns a value which makes datetime.datetime.fromtimestamp() happy.\n\nIt simply rewinds the code in the standard library's uuid1 function:\n\n    nanoseconds = int(time() * 1e9)\n    # 0x01b21dd213814000 is the number of 100-ns intervals between the\n    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.\n    timestamp = int(nanoseconds/100) + 0x01b21dd213814000\n