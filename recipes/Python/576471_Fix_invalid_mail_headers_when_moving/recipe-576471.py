#!/usr/bin/env python

"""Removes ">From" and "From " lines from mail headers.

Thunderbird adds invalid mail headers.  Cyrus IMAP is strict about them.  This
script walks through all files in the given directories and removes any line
that starts with ">From" or "From " (no colon).

Real "From:" lines must have the colon.

"""


from __future__ import with_statement
from sys import argv, exit, stderr
from os import listdir
from os.path import abspath, normpath, join, isfile, basename
from tempfile import mkdtemp
from contextlib import contextmanager
from shutil import rmtree, move


class FixMailHeadersError(Exception):

    """Base class for all exceptions in this module.

    This is different than the standard Exception class, in that sub-classes
    should define a _default_message attribute with the default message to
    present to the user.

    If not message is given at instantiation time, then the default message is
    used automatically.

    Also, note that only one argument (the message) can be given when
    instantiating these exceptions.

    """

    _default_message = u'Kaboom!' # override me!

    def __init__(self, message=None):
        """Set the given message or the default message is one is not given."""
        super(FixMailHeadersError, self).__init__(message if message is not
          None else self._default_message)


class InsufficientDirectories(FixMailHeadersError):

    """At least one directory must be given to clean_headers for it to work."""

    _default_message = u'You must specify at least one mail directory to scan.'


def get_file_paths(*dir_paths):
    """Yields all non-hidden, non-backup files in each given directory."""
    for dir_path in dir_paths:
        dir_path = abspath(normpath(dir_path))
        for file_name in listdir(unicode(dir_path)):
            file_path = join(dir_path, file_name)
            if (isfile(file_path) and not file_name.startswith(u'.') and not
              file_name.endswith(u'~')):
                yield file_path


@contextmanager
def make_temp_dir():
    """Context manager that creates and removes a temporary directory.

    All contents are also removed.

    """
    temp_dir_path = mkdtemp()
    try:
        yield temp_dir_path
    finally:
        rmtree(temp_dir_path)


def filter_file(in_file_path, temp_dir_path, filter=None):
    """Runs each line of the file through the given filter.

    The original files is backed up with a "~" added to the end of the file
    name.

    During processing a temporary file, with the same name as as the file to
    process, is created in the given temporary directory.  It only replaces the
    original file if there are no errors.

    """
    temp_file_path = join(temp_dir_path, basename(in_file_path))
    with open(in_file_path, 'r') as in_file:
        with open(temp_file_path, 'w') as temp_file:
            for line in in_file:
                if filter is None or filter(line):
                    temp_file.write(line)
    move(in_file_path, in_file_path + u'~')
    move(temp_file_path, in_file_path)


def _default_filter(line):
    """Default bad header filter.

    Filters out lines that start with ">From" or "From " (no colon).

    """
    line = line.strip()
    return (False if line.startswith('>From') or line.startswith('From ') else
      True)


def clean_headers(dir_paths, filter=_default_filter):
    """Remove bad header lines from all mail files in all given directories.

    Bad header lines are lines that start with ">From" or "From " (no colon) as
    created by Thunderbird. :(

    You can override this behaviour by providing yoru own filter callable.  It
    should accept a text line as the only argument and return True to keep the
    line and false to omit it.

    Directories are *not* recursed.  You must specify each directory
    explicitly.

    This is the function to call if you are using this module as a library
    rather than a command-line script.

    An exception is raised if no directory paths are given.

    This is a generator.  It first yields the file it's going to process next,
    and then on the next iteration, processes that file and yields the next
    file name to process.  This way you can provide feedback to the user before
    each file is processed.

    You can cause a file to be skipped by sending a true value into the
    generator instead of just calling next().

    """
    if not dir_paths:
        raise InsufficientDirectories()
    with make_temp_dir() as temp_dir_path:
        for file_path in get_file_paths(*dir_paths):
            if not (yield file_path):
                filter_file(file_path, temp_dir_path, filter)


def main(dir_paths):
    """Main function called when running as a command-line script.

    Progress and errors are printed to stdout and stderr, respectively.

    """
    try:
        for file_path in clean_headers(dir_paths):
            print file_path
    except FixMailHeadersError, error:
        print >>stderr, error
        exit(-1)


if __name__ == '__main__':
    main(argv[1:])
