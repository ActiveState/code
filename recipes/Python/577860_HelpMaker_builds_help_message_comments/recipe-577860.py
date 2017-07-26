""" HelpMaker: Builds help message from comments in the code.
"""
"""
    There are two types of help messages:
        the general help,
        and the specific helps to corresponding functions/commands.

    The general help message is the first comment in the .py file,
    wrapped by the triple-double-quotes.
    The general help describes what the .py file is about, or gives a brief
    introduction of the module.

    A specific help message is wrapped by the triple-double-quotes, and has only
    one word (no space in between) in the first line of the comment.
    A specific help explains/illustrates the usage of a function/command.
    The specific helps are stored in an internal dictionary. The only-one-word
    in the first line of comment serves as the key to the help message in the
    internal dictionary.
"""

import sys
import re

class Phase:
    HAVE_NOTHING = 0
    HAVE_GENERAL_MSG = 1
    HAVE_SPECIFIC_MSG = 2

class HelpMaker:
    def __init__(self, filename):
        """ construct function
            construction function that takes the name of the .py file.
            The function screens the entire file and gets ready to
            display the comments as help messages.
        """
        try:
            with open(filename) as pyfile:
                self._comment_head = re.compile(r"""^\s*\"{3}""")
                self._key_word = re.compile(r"""^\s*\"{3}\s*\S{1,}\s*\Z""")
                self._phase = Phase.HAVE_NOTHING
                self._is_comment = False
                self._general_help = ''
                self._specific_help = dict()
                self._tmp_key = ''
                self._tmp_msg = ''
                self._tmp_index = 0

                for line in pyfile:
                    if self._phase is Phase.HAVE_NOTHING:
                        self._general_help_filter(line)
                    elif self._phase is Phase.HAVE_GENERAL_MSG:
                        self._specific_help_filter(line)
        except IOError:
            print('Could not find the file: %s'%filename)

    """ available_help
        Generate all the items with help messages
    """
    def available_help(self):
        return self._specific_help.keys()

    def show_help(self, showitem = None):
        """ show_help
            Without any input this funtion shows general common help message.
            When the showitem is given, the corresponding help message will be
            displayed, if exists.
        """
        if showitem is None:
            print(self._general_help)
        else:
            try:
                print(self._specific_help[showitem])
            except KeyError:
                print('No help on %s available'%showitem)

    def _general_help_filter(self, line):
        """ helper function that finds out the general help message
        """
        if self._comment_head.search(line) is not None:
            self._tmp_indent = line.find('"') + 3
            self._is_comment = not self._is_comment

        if self._is_comment is True:
            self._general_help += line[self._tmp_indent:]

        if self._general_help is not '' and self._is_comment is False:
            self._phase = Phase.HAVE_GENERAL_MSG

    def _specific_help_filter(self, line):
        """ helper function that finds out the speific help message
        """
        if self._key_word.search(line) is not None:
            self._tmp_indent = line.find('"') + 3
            self._tmp_key = line[self._tmp_indent:].strip()
            self._is_comment = True
            return

        if self._is_comment is True:
            if self._comment_head.search(line) is not None:
                self._specific_help[self._tmp_key] = self._tmp_msg
                self._tmp_msg = ''
                self._is_comment = False
            else:
                self._tmp_msg += line[self._tmp_indent:]

if __name__ == '__main__':
    hm = HelpMaker(sys.argv[0])
    print('General help of HelpMaker:')
    hm.show_help()

    print("Functions with help message:")
    for item in hm.available_help():
        print(item)
    print('')
    print('Specific help of HelpMaker:show_help():')
    hm.show_help('show_help')
    print('Specific help of a nonexist function:')
    hm.show_help('nonsense')
