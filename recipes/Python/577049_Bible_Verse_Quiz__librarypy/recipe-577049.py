#! /usr/bin/env python
"""Automate the indexing and processing of the verse library.

These three classes allow a library directory to automatically be
parsed and prepared for use in a categorized reference database."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import os

################################################################################

class VerseLibrary:

    """Generate a verse reference database from a directory path.

    Given a directory that has been specially formatted, this class will
    index its files along with one layer of subdirectories. An XHTML index
    suitable for a form is automatically generated from the collected data."""

    def __init__(self, path):
        """Initialize variables from data on path."""
        self.__option = _VerseGroup(path)
        self.__groups = []
        for name in os.listdir(path):
            path_name = os.path.join(path, name)
            if os.path.isdir(path_name):
                self.__groups.append(_VerseGroup(path_name, name))
        self.__groups.sort(key=lambda group: group.title)
        self.__cache = self.__cache()

    def __cache(self):
        """Generate an XHTML menu from collected information.

        This method is here to organize the construction process of a
        VerseLibrary instance. A menu is cached and bound to this name."""
        cache = '<select id="{0}" name="{0}">\n{1}'
        template = '        <option value="{}.{}">{}</option>\n'
        for gi, group in enumerate(self.__groups):
            cache += '    <optgroup label="{}">\n'.format(group.title)
            for fi, file in enumerate(group):
                cache += template.format(gi, fi, file.title)
            cache += '    </optgroup>\n'
        template = '    <option value="{}">{}</option>\n'
        for fi, file in enumerate(self.__option):
            cache += template.format(fi, file.title)
        return cache + '</select>'

    def html(self, name, default=None):
        """Provide customized HTML code for the library menu.

        After taking the name of this portion of a form and an optional
        prompt, the cached HTML code (or XHTML) is reformatted to include
        the extra information. The results are then returned to the caller."""
        if default is None:
            S = ''
        else:
            S = '    <option selected="selected">{}</option>\n'.format(default)
        return self.__cache.format(name, S)

    def __contains__(self, item):
        """Verify if the item is contained in the groups.

        A string is taken in and parsed to see if it could possibly
        refer to a file contained in one of the groups. Various checks
        are run, and the result is returned via the "X in Y" syntax."""
        if item is None or item.count('.') > 1:
            return False
        if '.' in item:
            group, file = item.split('.', 1)
        else:
            group, file = None, item
        if group is None:
            group = self.__option
        else:
            try:
                group = self.__groups[int(group)]
            except (ValueError, IndexError):
                return False
        try:
            return 0 <= int(file) < len(group)
        except ValueError:
            return False

    def __getitem__(self, key):
        """Retrieve a file from one of the contained groups.

        The key is verified in order to make certain assumptions later on.
        If it is valid, the correct file is returned after parsing the key."""
        if key not in self:
            raise KeyError(repr(key) + ' NOT FOUND IN LIBRARY')
        if '.' in key:
            group, file = list(map(int, key.split('.')))
        else:
            group, file = None, int(key)
        if group is None:
            group = self.__option
        else:
            group = self.__groups[group]
        return group[file]

################################################################################

class _VerseGroup:

    """Collect and store a verse file index from a directory.

    Instances of this class are automatically built when they are needed
    by VerseLibrary. This an intermediate storage system for _VerseFiles."""

    def __init__(self, path, title=None):
        """Initialize instance's variables from information in directory."""
        self.__title = title
        self.__files = []
        for name in os.listdir(path):
            if os.path.splitext(name)[1].lower() == '.txt':
                path_name = os.path.join(path, name)
                if os.path.isfile(path_name):
                    self.__files.append(_VerseFile(path_name))
        self.__files.sort(key=lambda file: file.title)

    def __len__(self):
        """Provide the total number of files this _VerseGroup contains."""
        return len(self.__files)

    def __getitem__(self, key):
        """Index into the files and retrieve the one specified by the key."""
        return self.__files[key]

    def __iter__(self):
        """Generate an iterator over the files found in this _VerseGroup."""
        return iter(self.__files)

    @property
    def title(self):
        """Read-only title property identifying the group's contents."""
        return self.__title

################################################################################

class _VerseFile:

    """Cache the contents of a files along with its name.

    This class is used by _VerseGroup as needed. It stores the contents
    of text files and will automatically parse references when indexing."""

    # A copy of this can be found at database.BibleServer.BOOKS
    BOOKS = ('Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
             'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings',
             '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah',
             'Esther', 'Job', 'Psalm', 'Proverbs', 'Ecclesiastes',
             'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations',
             'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah',
             'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai',
             'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John',
             'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians',
             'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
             '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
             'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John',
             '3 John', 'Jude', 'Revelation')

    def __init__(self, path):
        """Initialize using non-empty lines from file on path."""
        self.__title = os.path.splitext(os.path.basename(path))[0]
        self.__lines = []
        for line in open(path):
            real = line.replace('\n', '')
            if real:
                self.__lines.append(real)

    def __getitem__(self, key):
        """Index into file's lines and get a parsed reference back."""
        if key not in self:
            raise KeyError('{}[{!r}]'.format(self.__class__.__name__, key))
        line = self.__lines[int(key)]
        return self.__parse(line)

    def __parse(self, line):
        """Split the reference into book, chapter, and verse range."""
        try:
            book, addr = line.rsplit(' ', 1)
            book = self.BOOKS.index(book) + 1
            if ':' not in addr:
                return book, int(addr), None, None
            chap, vers = addr.split(':')
            chap = int(chap)
            if '-' in vers:
                vers_a, vers_b = list(map(int, vers.split('-')))
            else:
                vers_a = vers_b = int(vers)
            return book, chap, vers_a, vers_b
        except:
            return None, None, None, None

    def __delitem__(self, key):
        """Delete the verse reference line specified by the key."""
        if key not in self:
            raise KeyError('{}[{!r}]'.format(self.__class__.__name__, key))
        del self.__lines[int(key)]

    def __iter__(self):
        """Create an iterator over the references in the verse file."""
        return iter(self.__lines)

    def __contains__(self, item):
        """Verify if the given string can refer to a line in the file."""
        try:
            index = int(item)
        except ValueError:
            return False
        else:
            return 0 <= index < len(self.__lines)

    @property
    def title(self):
        """Read-only title property identifying this file's contents."""
        return self.__title
