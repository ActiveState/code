## TimedCompressedRotatingFileHandler

Originally published: 2007-02-28 08:16:44
Last updated: 2007-02-28 08:16:44
Author: Angel Freire

Python has really nice logging framework, it has too a zipfile library in the default installation that makes you able to write compressed files.\n\nSeveral of the logging handlers "rotate" files, by size, date, etc. Here is an example of handler class for the logging framework that, when the file is rotated, it will make a .zip of the old file.