###Yet Another NamedTuple

Originally published: 2014-08-02 02:56:11
Last updated: 2014-08-02 02:56:12
Author: Steven D'Aprano

Yet another look at Raymond Hettinger's excellent "namedtuple" factory. Unlike Raymond's version, this one minimizes the use of exec. In the original, the entire inner class is dynamically generated then exec'ed, leading to the bulk of the code being inside a giant string template. This version uses a regular inner class for everything except the __new__ method.\n