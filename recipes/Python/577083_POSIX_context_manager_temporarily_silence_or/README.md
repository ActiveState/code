## POSIX context manager to temporarily silence, or filter lines from stdout  
Originally published: 2010-03-03 04:31:03  
Last updated: 2010-03-03 06:17:23  
Author: pwaller   
  
Fed up with libraries you don't have control over emitting text into your precious stdout?

If they use stdout through python, then you can just change sys.stdout to be something else. If they are printing directly to stdout through a C module, or some other means, then you are stuck.

.. at least until you discover the `with silence():` block!

Caveats: Non-portable, tested only on 2.6 under Linux, uses threading.

Example output:

    $ python silence_file.py 
    Before with block..
    Sensible stuff!
    After the silence block
