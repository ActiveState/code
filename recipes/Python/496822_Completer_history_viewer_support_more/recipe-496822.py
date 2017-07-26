# History.py
#
# Store the file "History.py"
# in site-packages directory like "/usr/lib/python2.4/site-packages,"
# or a directory pointed by PYTHONPATH environment varable,
# or your home directory.
#
# Insert the line, "import History" to "~/.pystartup" file,
# and set an environment variable to point to it:
# "export PYTHONSTARTUP=${HOME}/.pystartup" in bash.
#
# References:
#     Guido van Rossum. Python Tutorial. Python Sfotware Foundation, 2005. 86
#     Jian Ding Chen. Indentable rlcompleter. Python Cookbook Recipe 496812
#     Guido van Rossum. rlcompleter.py. Python Sfotware Foundation, 2005
#
# 2006.06.29 Sunjoong LEE <sunjoong@gmail.com>
#
__author__ = 'Sunjoong LEE <sunjoong@gmail.com>'
__date__ = '2006-06-29'
__version__ = '1.0'


from atexit import register
from itertools import count as icount, ifilter, imap
from os import listdir, remove
from os.path import exists, expanduser, split as psplit
from readline import clear_history, get_current_history_length, \
     get_completer_delims, get_history_item, get_line_buffer, \
     insert_text, parse_and_bind, read_history_file, redisplay, \
     set_completer, set_completer_delims, set_history_length, \
     set_pre_input_hook, write_history_file
from pwd import getpwall
from rlcompleter import Completer
from tempfile import mktemp

import __main__


historyPath = expanduser('~/.pyhistory')
HISTORY_LENGTH = 100




class History:
    def __init__(self):
        self.recall()
        set_history_length(HISTORY_LENGTH)

        parse_and_bind('tab: complete')
        # delims = get_completer_delims()
        delims = ' \t\n`!@#$%^&*()-=+[{]}\\|;:,<>?'
        set_completer_delims(delims)
        set_completer(irlcompleter().complete)


    def __repr__(self):
        """print out current history information"""
        command = get_history_item(get_current_history_length())
        if command == 'history':
            length = get_current_history_length()
            if length > 1:
                return reduce(lambda x, y: '%s\n%s' % (x, y),
                              imap(get_history_item, xrange(1, length)))
            else:
                return ''
        else:
            return '<%s instance>' % __name__


    def __call__(self):
        """print out current history information with line number"""
        length = get_current_history_length()
        if length > 1:
            kount = icount(1).next
            for command in imap(get_history_item, xrange(1, length)):
                print '%s\t%s' % (kount(), command)


    def save(self, filename, pos = None, end = None):
        """write history number from pos to end into filename file"""
        length = get_current_history_length()
        if length > 1:
            if not pos:
                pos = 1
            elif pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end:
                end = length
            elif end >= length:
                end = length
            if end < 0:
                end = length + end
            else:
                end = end + 1

            fp = open(filename, 'w')
            write = fp.write
            if pos < end:
                map(lambda x: write('%s\n' %  x),
                    imap(get_history_item, xrange(pos, end)))
            else:
                write('%s\n' % get_history_item(pos))
            fp.close()


    def clear(self):
        """save the current history and clear it"""
        write_history_file(historyPath)
        clear_history()


    def recall(self, historyPath = historyPath):
        """clear the current history and recall it from saved"""
        clear_history()
        if exists(historyPath):
            read_history_file(historyPath)


    def execute(self, pos, end = None):
        """execute history number from pos to end"""
        length = get_current_history_length()
        if length > 1:
            if pos >= length - 1:
                pos = length - 1
            elif pos < 1:
                pos = length + pos - 1
            if not end:
                end = pos + 1
            elif end >= length:
                end = length
            if end < 0:
                end = length + end
            else:
                end = end + 1

            to_execute = map(get_history_item, xrange(pos, end))

            filename = mktemp()
            fp = open(filename, 'w')
            write = fp.write
            map(lambda x: write('%s\n' % x), to_execute.__iter__())
            fp.close()

            try:
                execfile(filename, __main__.__dict__)
                read_history_file(filename)
                remove(filename)
            except:
                remove(filename)




class irlcompleter(Completer):
    def complete(self, text, state):
        if text == '':
            # you could replace '    ' to \t if you indent via tab
            return ['    ', None][state]
        elif text.count("'") == 1:
            if not state:
                self.file_matches(text, "'")
            try:
                return self.matches[state]
            except IndexError:
                return None
        elif text.count('"') == 1:
            if not state:
                self.file_matches(text, '"')
            try:
                return self.matches[state]
            except IndexError:
                return None
        else:
            return Completer.complete(self, text, state)


    def file_matches(self, text, mark):
        if '~' in text:
            if '/' in text:
                text = '%s%s%s' % (mark, expanduser(
                    text[text.find('~'):text.find('/')]),
                                   text[text.find('/'):])
            else:
                self.user_matches(text, mark)
                return

        text1 = text[1:]
        delim = '/'

        if not text1:
            directory = ''
        elif text1 == '.':
            directory = '.'
        elif text1 == '..':
            directory = '..'
        elif text1 == '/':
            directory = '/'
            delim = ''
        elif text1[-1] == '/':
            directory = text1[:-1]
            delim = text1[len(directory):]
        else:
            directory, partial = psplit(text1)
            delim = text1[len(directory):][:-len(partial)]

        if directory:
            listing = map(lambda x: '%s%s%s%s' % (mark, directory, delim, x),
                          listdir(directory).__iter__())
        else:
            listing = map(lambda x: '%s%s' % (mark, x),
                          listdir('.').__iter__())

        n = len(text)
        self.matches = filter(lambda x: x[:n] == text, listing.__iter__())


    def user_matches(self, text, mark):
        n = len(text)
        self.matches = filter(lambda x: x[:n] == text,
                              imap(lambda x: '%s~%s' % (mark, x[0]),
                                   getpwall().__iter__()))




def save_history(historyPath = historyPath):
    from readline import write_history_file
    write_history_file(historyPath)
register(save_history)


def hook():
    from readline import set_pre_input_hook
    import __main__
    set_pre_input_hook()
    delattr(__main__, 'History')
    delattr(__main__, '__file__')
set_pre_input_hook(hook)
setattr(__main__.__builtins__, 'history', History())
