## BaseDict -- a dict that (1) accesses data thru attributing (2) copy correctly  
Originally published: 2006-01-26 15:11:58  
Last updated: 2006-01-27 06:44:54  
Author: runsun pan  
  
<code>A dict extension that has the following features:

    1. dual data storages: use 'bd.x' or 'bd["x"]' for one,
       and bd.getDict() for another.

    2. All the followings are equivalent::

           bd['x']= val
           bd.x   = val
           bd.setItem('x', val)  # Return bd

    3. bd.setDict('x',val) will save 'x' to bd.__dict__,
       but not bd.items

    4. When copy, copy the internal object correctly.
</code>