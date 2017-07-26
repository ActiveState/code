###A ThunkSpace for Python

Originally published: 2006-01-04 00:20:26
Last updated: 2006-01-04 08:45:19
Author: S W

This useless hack allows normal functions to be attached to a 'ThunkSpace' which causes the function to be lazily evaluated when the thunk is referenced. It is just a experiment using closures and descriptors to try and change python function call syntax.