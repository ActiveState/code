#! /usr/bin/env python
"""Run a Bible-verse-matching servlet on the network.

This program is a port of the VerseMatch program written
in CPS 110 at BJU during the Autumn Semester of 2003."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '11 February 2010'
__version__ = '$Revision: 3 $'

################################################################################

# File: VerseList.py
# Description: A simple "VerseList" servlet

import os
import sys
import servlet
import manager
import library
import database
import verse
import html

################################################################################

from state import State

indent = lambda S, I: '\n'.join(' ' * I + line for line in S.split('\n'))
    
################################################################################

class VerseMatch(servlet.HttpServlet):

    """Create a handler responsible for the application.

    This is a port of the VerseMatch class in the first Java program.
    The service method gets called each time a HTTP request is made."""
    
    __init = False  # Tracks if VerseMatch was initialized.

    @classmethod
    def init(cls, lib_path, db_path):
        """Initialize static variables so this class can be used.

        The session manager cleans memory of old sessions not in use.
        The library keeps Bible references and generates related HTML.
        The Bible server responds to verse queries with Verse objects."""
        assert not cls.__init, 'VerseMatch is already initialized!'
        # Session Manager closes old sessions each hour.
        cls.SM = manager.SessionManager(3600)
        cls.SM.daemon = True
        cls.SM.start()
        cls.LIBRARY = library.VerseLibrary(lib_path)
        cls.BIB_SVR = database.BibleServer(db_path)
        cls.__init = True
        # "testverse.Verse.init_manager" should be called
        # somewhere to ensure that verse checks are killed.
        verse.Verse.init_manager(5) # Runs every 5 seconds.

################################################################################

    def service(self, request, response):
        """Handle GET and POST requests from client's browser."""
        assert self.__init, 'VerseMatch was never initialized!'
        state = self.get_state()
        # Handle action desired by the client.
        action = request.getParameter('action')
        state = self.exe_action(action, state, request)
        # Render HTML specified by current state.
        response.setContentType('text/html')
        out = response.getWriter()
        code = self.render_html(state)
        out.print(code)

    def get_state(self):
        """Get state of client's specific application instance.

        The client's IP address is used for identity purposes.
        If there is a session associated with the client, the
        session's state is returned for further processing.
        Otherwise, a new session is created with a new state
        object being added to it, and the new state is returned."""
        ip = self.client_address[0]
        with self.SM:
            if ip in self.SM:
                session = self.SM[ip]
            else:
                # Sessions may live for up to 24 hours.
                session = manager.Session(86400)
                session.state = State(session, self.LIBRARY, self.BIB_SVR)
                session.ip = ip
                self.SM[ip] = session
        return session.state

    def exe_action(self, action, state, request):
        """Execute the action specified by the caller.

        This application recognizes several actions that the
        client may freely attempt to invoke. If the action is
        recognized, relevant methods are called on the state
        object with needed parameter being queried as needed."""
        if action == 'Go Back':
            state.go_back()
        elif action == 'Reset Session':
            # This session is being deleted and new one made.
            state.reset_session()
            state = self.get_state()
        elif action == 'Choose Quiz':
            # Form created by LIBRARY should be called "quiz."
            quiz_id = request.getParameter('quiz')
            state.load_quiz(quiz_id)
        elif action == 'pickverse':
            # Query: "action=pickverse&id=X" where X is a number.
            verse_id = request.getParameter('id')
            state.pick_verse(verse_id)
        elif action == 'Check Your Answer':
            verses = []
            for verse in range(state.verse_total):
                text = request.getParameter('verse' + str(verse))
                verses.append(text)
            state.check_text(verses)
            self.__status = 0
        elif action == 'checkstatus':
            self.__status = state.check_status()
        return state

    def render_html(self, state):
        """Render the XHTML of the current state.

        Depending on the state of a client's session,
        one of several different pages may be sent to
        his browser. The correct page is selected and
        rendered here along with XHTML code that may
        need to be dynamically generated on the fly."""
        if state.current == State.OPTIONS.GET_QUIZ:
            select = indent(self.LIBRARY.html('quiz', 'Options:'), 16)
            get_quiz = html.GET_QUIZ.format(select)
            template = html.TEMPLATE.format('', get_quiz)
        elif state.current == State.OPTIONS.GET_VERSE:
            title, menu = self.render_menu(state)
            get_verse = html.GET_VERSE.format(title, menu)
            template = html.TEMPLATE.format('', get_verse)
        elif state.current == State.OPTIONS.TEACH:
            area = self.render_area(state)
            teach = html.TEACH.format(area)
            template = html.TEMPLATE.format('', teach)
        else:
            assert state.current == State.OPTIONS.CHECK
            args = ((self.__status if self.__status else 'No'),
                    (' has' if self.__status == 1 else 's have'))
            check = html.CHECK.format(*args)
            template = html.TEMPLATE.format(html.REFRESH, check)
        return template

    def render_menu(self, state):
        """Create a Bible verse selection menu.

        The second page of the application (GET_VERSE)
        displays a menu for selecting verses from the
        currently selected quiz set. The XHTML code for
        that menu is dynamically generated in this method."""
        file = state.verse_file
        form = '<li>\n    <a href="?action=pickverse&id={}">{}</a>\n</li>'
        ulli = '<ul>\n'
        for args in enumerate(file):
            ulli += indent(form.format(*args), 4) + '\n'
        ulli += '</ul>'
        return file.title, indent(ulli, 16)

    def render_area(self, state):
        """Create code for verse entry boxes.

        The third page of the application (called TEACH)
        requires textarea XHTML code for individual verses
        to be entered in. The relavent fieldset, legend, and
        status codes are added to the template and returned."""
        verses = []
        span = '''
                <span style="color: {};">{}</span>
                <br />'''
        for index, verse in enumerate(state.verse_list):
            if verse.show_hint:
                text, status = self.render_status(verse, span)
            else:
                text = status = ''
            args = verse.addr, status, 'verse' + str(index), text
            verses.append(html.VERSE.format(*args))
        return '\n'.join(verses)

    def render_status(self, verse, span):
        """Compute the status of verse in question.

        Each verse has an optional status to show on the
        TEACH page. This method figures out what to show
        (if anything) and decides what the verse hint is."""
        if verse.ready is True:
            right, total, text = verse.value
            if right == total:
                status = span.format('#0A0', 'You know this verse perfectly!')
            elif right > 0:
                string = 'You already know {}% of this verse.'
                correct = string.format(int(100 * right / total))
                status = span.format('#00A', correct)
            else:
                status = span.format('#00A', 'Here is a hint for this verse.')
        else:
            text = verse.hint
            status = span.format('#A00', 'Your answer took too long to check!')
        return text, status

################################################################################

def main():
    """Initialize program variables and start the server."""
    # Initialize verse database and libary.
    os.chdir(os.path.dirname(sys.argv[0]))
    VerseMatch.init('Quizes', 'bible13.db')
    # Start servlet with debugging enabled.
    servlet.HttpServlet.debug(True)
    servlet.HttpServer.main(VerseMatch, 8080)

################################################################################

if __name__ == '__main__':
    main()
