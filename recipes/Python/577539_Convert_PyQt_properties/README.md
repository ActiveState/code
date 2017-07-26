## Convert PyQt properties to Python properties

Originally published: 2011-01-09 01:51:28
Last updated: 2011-01-09 02:02:30
Author: Miguel Turner

This recipe will find all attributes created as meta-object properties in Qt and will create a Python property of the same name for each of them. This is a quick way of providing some of the functionality suggested by [PSEP 102](http://www.pyside.org/docs/pseps/psep-0102.html), which I sincerely hope will be accepted, as it will make PySide considerably more pythonic.