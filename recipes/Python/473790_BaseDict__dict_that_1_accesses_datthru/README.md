###BaseDict -- a dict that (1) accesses data thru attributing (2) copy correctly

Originally published: 2006-01-26 15:11:58
Last updated: 2006-01-27 06:44:54
Author: runsun pan

<code>A dict extension that has the following features:\n\n    1. dual data storages: use 'bd.x' or 'bd["x"]' for one,\n       and bd.getDict() for another.\n\n    2. All the followings are equivalent::\n\n           bd['x']= val\n           bd.x   = val\n           bd.setItem('x', val)  # Return bd\n\n    3. bd.setDict('x',val) will save 'x' to bd.__dict__,\n       but not bd.items\n\n    4. When copy, copy the internal object correctly.\n</code>