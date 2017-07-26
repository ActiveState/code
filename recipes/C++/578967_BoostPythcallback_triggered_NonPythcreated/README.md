## Boost::Python callback triggered from Non-Python created threads

Originally published: 2014-11-20 20:00:26
Last updated: 2014-11-20 20:00:27
Author: Tomáš Rampas

Consider  we have virtual/abstract C++ class that's fully implemented in Python. And for some sake of necessity we have a callback method (e.g. as some sort of event) that is being triggered from different thread on C++ side.\nIn such case corresponding callback methods have to manage GIL state via PyGILState_STATE.\nSo the resulting C++ callback class definition will look like follows (notice that Python method calls are wrapped up with GIL state handling code).