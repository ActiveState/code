# -*- coding: iso-8859-1 -*-
"""
Handling of arguments: options, arguments, file(s) content iterator

For small scripts that:
- read some command line options
- read some command line positional arguments
- iterate over all lines of some files given on the command line, or stdin if none given
- give usage message if positional arguments are missing
- give usage message if input files are missing and stdin is not redirected
"""

__author__ = 'Peter Kleiweg'
__version__ = '0.2'
__date__ = '2004/08/28'

import os, sys, getopt

class Args:
    """
    Perform common tasks on command line arguments
    
    Instance data:
    progname (string) -- name of program
    opt (dictionary) -- options with values
    infile (string) -- name of current file being processed
    lineno (int) -- line number of last line read in current file
    linesum (int) -- total of lines read
    """

    def __init__(self, usage='Usage: %(progname)s [opt...] [file...]'):
        "init, usage string: embed program name as %(progname)s"
        self.progname = os.path.basename(sys.argv[0])
        self.opt = {}
        self.infile = None
        self.lineno = 0
        self.linesum = 0
        self._argv = sys.argv[1:]
        self._usage = usage

    def __iter__(self):
        "iterator: set-up"
        if self._argv:
            self.infile = self._argv.pop(0)
            self._in = open(self.infile, 'r')
            self._stdin = False
        else:
            if sys.stdin.isatty():
                self.usage()  # Doesn't return
            self.infile = '<stdin>'
            self._in = sys.stdin
            self._stdin = True
        return self

    def next(self):
        "iterator: get next line, possibly from next file"
        while True:
            line = self._in.readline()
            if line:
                self.lineno += 1
                self.linesum += 1
                return line

            if self._stdin:
                break

            self._in.close()
            try:
                self.infile = self._argv.pop(0)
            except IndexError:
                break
            self.lineno = 0
            self._in = open(self.infile, 'r')

        self.lineno = -1
        self.infile = None
        raise StopIteration

    def getopt(self, shortopts, longopts=[]):
        "get options and merge into dict 'opt'"
        try:
            options, self._argv = getopt.getopt(self._argv, shortopts, longopts)
        except getopt.GetoptError:
            self.usage()
        self.opt.update(dict(options))

    def shift(self):
        "pop first of remaining arguments (shift)"
        try:
            return self._argv.pop(0)
        except IndexError:
            self.usage()

    def pop(self):
        "pop last of remaining arguments"
        try:
            return self._argv.pop()
        except IndexError:
            self.usage()

    def warning(self, text):
        "print warning message to stderr, possibly with filename and lineno"
        if self.lineno > 0:
            print >> sys.stderr, '%s:%i: warning: %s' % (self.infile, self.lineno, text)
        else:
            print >> sys.stderr, '\nWarning %s: %s\n' % (self.progname, text)

    def error(self, text):
        "print error message to stderr, possibly with filename and lineno, and exit"
        if self.lineno > 0:
            print >> sys.stderr, '%s:%i: %s' % (self.infile, self.lineno, text)
        else:
            print >> sys.stderr, '\nError %s: %s\n' % (self.progname, text)
        sys.exit(1)

    def usage(self):
        "print usage message, and exit"
        print >> sys.stderr
        print >> sys.stderr, self._usage % {'progname': self.progname}
        print >> sys.stderr        
        sys.exit(1)


if __name__ == '__main__':

    a = Args('Usage: %(progname)s [-a value] [-b value] [-c] word [file...]')

    a.opt['-a'] = 'option a'    # set some default option values
    a.opt['-b'] = 'option b'    #
    a.getopt('a:b:c')           # get user supplied option values

    word = a.shift()            # get the first of the remaining arguments
                                # use a.pop() to get the last instead

    for line in a:              # iterate over the contents of all remaining arguments (file names)
        if a.lineno == 1:
            print 'starting new file:', a.infile
        a.warning(line.rstrip())

    print 'Options:', a.opt
    print 'Word:', word
    print 'Total number of lines:', a.linesum

    print 'Command line:', sys.argv     # unchanged

    a.warning('warn 1')         # print a warning
    a.error('error')            # print an error message and exit
    a.warning('warn 2')         # this won't show
