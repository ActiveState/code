'''Support module for use by CGI scripts.

This module provides several functions and variables
that help with printing text and accessing form data.'''

__version__ = 1.3

################################################################################

class File:
    def __init__(*args, **kwargs):
        pass
    def flush(*args, **kwargs):
        pass
    def isatty(*args, **kwargs):
        pass
    def write(*args, **kwargs):
        pass
    def writelines(*args, **kwargs):
        pass

################################################################################

import sys

out = sys.stdout
sys.stdout = File()

def execute(main, exception):
    'Execute main unless exception.'
    if exception != string:
        main()
    else:
        print_self()

def print_html(text):
    'Print text as HTML.'
    out.write('Content-Type: text/html\n\n' + text)
    sys.exit(0)

def print_plain(text):
    'Print text as plain.'
    out.write('Content-Type: text/plain\n\n' + text)
    sys.exit(0)

def print_self():
    'Print __main__ as plain.'
    print_plain(file(sys.argv[0]).read())

################################################################################

import os

def export():
    'Exports string and dictionary.'
    global string, dictionary
    try:
        string = str(os.environ['QUERY_STRING'])
    except:
        string = str()
    try:
        dictionary = dict([(decode(parameter), decode(value)) for parameter, value in [item.split('=') for item in string.replace('+', ' ').split('&')]])
    except:
        dictionary = dict()

def decode(string):
    'Receives, decodes, and returns string.'
    index = string.find('%')
    while index != -1:
        string = string[:index] + chr(int(string[index+1:index+3], 16)) + string[index+3:]
        index = string.find('%', index + 1)
    return string

################################################################################

if __name__ == '__main__':
    print_self()
else:
    export()
