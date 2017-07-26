#! /usr/bin/env python
"""Manage the state of a VerseMatch session.

If VerseMatch is the heart of the program, then state is the brain.
All user interactions are processed by the State class listed below."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

def enum(names):
    """Generate an enumeration with the given names.

    The names should be separated with commas and/or whitespace.
    A class is dynamically generated, and an instance is returned.
    Python does not support enumerations, so this is an alternative."""
    names = names.replace(',', ' ').split()
    space = dict((reversed(pair) for pair in enumerate(names)), __slots__=())
    return type('enum', (object,), space)()

################################################################################

class State:

    """Oversee state transitions in a VerseMatch session.

    This class controls clients' movements from state to state while
    navigating through their sessions. Commands are verified along with
    any arguments that they take. The VerseMatch servlet automatically
    creates State objects and adds them as attributes to Session objects."""

    # These are different states instances may be in.
    OPTIONS = enum('GET_QUIZ, GET_VERSE, TEACH, CHECK')

    def __init__(self, session, library, bib_svr):
        """Initialize resources to be used by this instance."""
        self.__session = session
        self.__library = library
        self.__bib_svr = bib_svr
        self.__state = self.OPTIONS.GET_QUIZ
        # These will be set again later on.
        self.__quiz_id = ''
        self.__verses = []

    def load_quiz(self, quiz_id):
        """Transition from getting quiz to getting verse.

        The first screen of the verse quiz allows the client to select what
        category of verses he would liked to be quizzed from. This method
        verifies that selection and moves on to the next phase if possible."""
        if self.__state == self.OPTIONS.GET_QUIZ:
            if quiz_id in self.__library:
                self.__state = self.OPTIONS.GET_VERSE
                self.__quiz_id = quiz_id

    def pick_verse(self, verse_id):
        """Move from picking the verse to teaching the verse.

        The second page that pops up in this application provides a menu
        to choose what verse(s) should be used for a quiz. The selected
        reference is verified; and if the verse could be found, a state
        change occurs. Othewise, the reference is removed from the list."""
        if self.__state == self.OPTIONS.GET_VERSE:
            file = self.__library[self.__quiz_id]
            if verse_id in file:
                bk, ch, v1, v2 = file[verse_id]
                if bk is None:
                    verses = None
                elif v1 is None:
                    verses = self.__bib_svr.fetch_chapter(bk, ch)
                elif v1 == v2:
                    verses = self.__bib_svr.fetch_verse(bk, ch, v1)
                else:
                    verses = self.__bib_svr.fetch_range(bk, ch, v1, v2)
                if verses is None:
                    del file[verse_id]
                else:
                    self.__verses = tuple(verses)
                    for verse in self.__verses:
                        verse.show_hint = False
                    self.__state = self.OPTIONS.TEACH

    def check_text(self, verses):
        """Begin checking the verses that were submitted.

        The text from the verse entry boxes is sent here for immediate
        grading. A verification engine is automatically started for
        each verse, and status messages are shown for boxes with content."""
        if self.__state == self.OPTIONS.TEACH:
            if self.__check_arg(verses):
                for text, verse in zip(verses, self.__verses):
                    verse.check(text, 15, self.__session.ip)
                    verse.show_hint = bool(text)
                self.__state = self.OPTIONS.CHECK

    def __check_arg(self, verses):
        """Verify that the argument given to check_text is valid."""
        if len(verses) != len(self.__verses):
            return False
        for verse in verses:
            if not isinstance(verse, str):
                return False
        return True

    def check_status(self):
        """Sum up each status from the different verse objects.

        Find out how many verses are being checked and how many
        have finished their checking procedure. If some are still
        being checked, the total that have finished is returned.
        Otherwise, the program goes back into its teaching mode."""
        if self.__state == self.OPTIONS.CHECK:
            checking = complete = 0
            for verse in self.__verses:
                status = verse.ready
                if status is False:
                    checking += 1
                elif status is True:
                    complete += 1
            if checking == 0:
                self.__state = self.OPTIONS.TEACH
            return complete

    def go_back(self):
        """Go back to a previous state if possible.

        It is impossible to go forward through the states without
        meeting certain requirements. Going backward is relatively
        easy with this method. Negative states are not allowed,
        and the verse-checking process may not be interrupted."""
        if self.__state != self.OPTIONS.CHECK:
            self.__state = max(0, self.__state - 1)

    def reset_session(self):
        """Destroy this state and start over from scratch.

        In actuality, the session that keeps this state instance is
        removed from the session manager (if it exists there). Note
        that a new state is generated before a response is sent out."""
        with self.__session.manager:
            if self.__session.ip in self.__session.manager:
                del self.__session.manager[self.__session.ip]

################################################################################

    @property
    def current(self):
        """Read-only current-state property for VerseMatch class."""
        return self.__state

    @property
    def verse_file(self):
        """Read-only verse-file property for VerseMatch class."""
        return self.__library[self.__quiz_id]

    @property
    def verse_total(self):
        """Read-only verse-total property for VerseMatch class."""
        return len(self.__verses)

    @property
    def verse_list(self):
        """Read-only verse-list property for VerseMatch class."""
        return tuple(self.__verses)
