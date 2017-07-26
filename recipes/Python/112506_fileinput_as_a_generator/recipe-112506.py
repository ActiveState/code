from __future__ import generators
"""Provides a class called LineIterator that iterates over every line in a list of files.

Performing the basic functionality as fileinput module in the standard 
library (which mimics Perl's <> operator).  Basically acts as a simple 
and methodical way to iterate over every line in a list of files.  If 
not files are specified at instance creation, then sys.argv[1:] is used.
If that is empty, then sys.stdin is used.  sys.stdin can be specified in 
the list of files by listing '-' as a file.

Lacking functionality, compared to the fileinput module, is in-place 
editing and subsequently backup.  The module functions that are included 
in fileinput are left out here for space concerns.  readline() has also 
been left out since the generator can just have its .next() method called.

Dedicated to my grandmother, Mary Alice Renshaw (1911/12/13-2002/01/13).

"""
import sys


__author__ = 'Brett Cannon'
__email__ = 'drifty@bigfoot.com'
__version__ = '1.0'


class LineIterator(object):
    """Basic  reimplementation of fileinput.FileInput using generators.

    Passed in files are iterated over (file by file, line by line), and
    returned by the iterator.  Use of sys.stdin is specified  by '-'.
    if no files are specified, sys.argv[1:] is used.  If that is empty,
    sys.stdin is used.

    Flags values (| values together; set by various methods):
    1 :: Close current file
    2 :: End generator (thus 3 closes the current file and ends the
         generator)

    """

    def __init__(self, file_list=sys.argv[1:]):
        """Set all instance variables.

        If no files are specified (either passed in or from sys.argv[1:]),
        then sys.stdin is then used by making the only file '-'.

        """
        if file_list:
            if isinstance(file_list,str):
                self.__file_list = [file_list]
            else:
                self.__file_list = file_list
        else:
            self.__file_list = list('-')
        self.__current_file=''
        self.__relative_cnt = 0
        self.__absolute_cnt = 0
        self.__flags = 0

    def nextfile(self):
        """Starts looping over next file."""
        self.__flags = 1

    def close(self):
        """Ends the generator.

        Does this by setting __flag to both close the current file and
        end the generator.

        """
        self.__flags = 3

    def filename(self):
        """Returns name of current file."""
        if self.__current_file == '-':
            return 'sys.stdin'
        else:
            return self.__current_file

    def lineno(self):
        """Returns accumulative line total thus far."""
        return self.__absolute_cnt

    def filelineno(self):
        """Returns line total for the current file thus far."""
        return self.__relative_cnt

    def __iter__(self):
        """Generator for looping over every line in the files in self.files.

        If __flag is set to &2, then end the generator.  Otherwise check if
        '-' (read: sys.stdin) is the next file.  Set __relative_cnt to 0 and
        start iterating.

        If __flag is set to &1, close the current file and break the loop.
        Else see if the file name equals the current file name.  If not,
        change it.  Then increment both __relative_cnt and __absolute_cnt.
        Finally, yield the line.

        """
        for file_location in self.__file_list:
            if self.__flags & 2:
                return
            if file_location == '-':
                FILE = sys.stdin
            else:
                FILE = open(file_location,'r')
            self.__relative_cnt = 0
            for line in FILE:
                if self.__flags & 1:
                    FILE.close()
                    break
                if file_location != self.__current_file:
                    self.__current_file = file_location
                self.__relative_cnt += 1
                self.__absolute_cnt += 1
                yield line
            else: FILE.close()
