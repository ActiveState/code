## PyChecker postprocessor

Originally published: 2008-02-20 12:32:05
Last updated: 2017-01-10 21:19:34
Author: Jean Brouwers

This recipe can separate the output of PyChecker, PyFlakes, PyCodeStyle (formerly Pep8) and/or McCabe into OK'd and regular warning messages.\n\nIf invoked from Python 3+, this recipe with run Flake8 by default.  Command line option -3 allows running Python 3+ versions of the checkers.  \n\nAn example is included further below.  See the module documentation or -help for more details, versions, etc.