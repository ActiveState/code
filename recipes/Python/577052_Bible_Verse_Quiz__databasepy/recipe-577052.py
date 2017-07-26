#! /usr/bin/env python
"""Serve verses from the Bible in response to SQL queries.

Pulling Bible verses out of a database allows query details to be
abstracted away and powerful Verse objects returned to the caller."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

import _thread
import sqlite3
import queue
import verse

################################################################################

class BibleServer:

    """Execute a protected SQLite3 database on a singular thread.

    Since a SQLite3 database can only accept queries on the thread that it
    was created on, this server receives requests through a queue and sends
    back the result through a list and mutex mechanism. The verses returned
    from queries are automatically wrapped in their own Verse objects."""

    # A copy of this can be found at library._VerseFile.BOOKS
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

    def __init__(self, *args):
        """Initialize the BibleServer with a SQLite3 database thread."""
        self.__lock = _thread.allocate_lock()
        self.__lock.acquire()
        _thread.start_new_thread(self.__serve, args)
        self.__lock.acquire()
        del self.__lock
        if self.__error is not None:
            raise self.__error
        del self.__error

    def __serve(self, *args):
        """Run a server continuously to answer SQL queries.

        A SQLite3 connection is made in this thread with errors being raised
        again for the instantiator. If the connection was made successfully,
        then the server goes into a continuous loop, processing SQL queries."""
        try:
            database = sqlite3.connect(*args)
        except:
            self.__error = error = sys.exc_info()[1]
        else:
            self.__error = error = None
        self.__lock.release()
        if error is None:
            self.__QU = queue.Queue()
            while True:
                lock, one, sql, parameters, ret = self.__QU.get()
                try:
                    cursor = database.cursor()
                    cursor.execute(sql, parameters)
                    data = cursor.fetchone() if one else cursor.fetchall()
                    ret.extend([True, data])
                except:
                    ret.extend([False, sys.exc_info()[1]])
                lock.release()

    def fetch_chapter(self, book, chap):
        """Fetch all verses from chapter and wrap in Verse objects."""
        rows = self.__fetch(False, '''select vers, text from verses where
        book=? and chap=? order by vers asc''', book, chap)
        return self.__verses(book, chap, rows)

    def fetch_verse(self, book, chap, vers):
        """Fetch one verse as specified and wrap in a Verse object."""
        row = self.__fetch(True, '''select text from verses where
        book=? and chap=? and vers=?''', book, chap, vers)
        if row is not None:
            return [verse.Verse(self.__addr(book, chap, vers), row[0])]

    def fetch_range(self, book, chap, vers_a, vers_b):
        """Fetch all verses in the range and wrap in Verse objects."""
        rows = self.__fetch(False, '''select vers, text from verses where
        book=? and chap=? and vers>=? and vers<=? order by vers asc''',
                            book, chap, vers_a, vers_b)
        return self.__verses(book, chap, rows)

    def __fetch(self, one, sql, *parameters):
        """Execute the specified SQL query and return the results.

        This is a powerful shortcut method that is the closest connection
        other threads will have with the SQL server. The parameters for the
        query are dumped into a queue, and the answer is retrieved when it
        becomes available. This prevents SQLite3 from throwing exceptions."""
        lock, ret = _thread.allocate_lock(), []
        lock.acquire()
        self.__QU.put((lock, one, sql, parameters, ret))
        lock.acquire()
        if ret[0]:
            return ret[1]
        raise ret[1]

    def __verses(self, book, chap, rows):
        """Wrap the text from the rows in Verse objects.

        If the query matched any verses, the verse reference is deduced and
        used with the verse text to construct an array of Verse objects."""
        if rows:
            verses = []
            for vers, text in rows:
                verses.append(verse.Verse(self.__addr(book, chap, vers), text))
            return verses

    def __addr(self, book, chap, vers):
        """Construct a verse reference from the final three parameters."""
        return '{} {}:{}'.format(self.BOOKS[book - 1], chap, vers)
