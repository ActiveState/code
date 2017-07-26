## 'with' statement for StringIO

Originally published: 2009-02-10 21:06:47
Last updated: 2009-02-24 00:01:16
Author: srid 

NOTE: Consider this recipe obsolete. Instead use `contextlib.closing` (see comment below).\n\nThis contextmanager adds 'with' statement support for StringIO. Peruse the following simple example:\n\n    with StringIO() as sio:\n        function_accepting_file_handle(sio)\n        print sio.getvalue()\n\n