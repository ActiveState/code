## 'with' statement for StringIO  
Originally published: 2009-02-10 21:06:47  
Last updated: 2009-02-24 00:01:16  
Author: srid   
  
NOTE: Consider this recipe obsolete. Instead use `contextlib.closing` (see comment below).

This contextmanager adds 'with' statement support for StringIO. Peruse the following simple example:

    with StringIO() as sio:
        function_accepting_file_handle(sio)
        print sio.getvalue()

