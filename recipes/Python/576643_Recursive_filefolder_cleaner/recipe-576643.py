#!/usr/bin/env python
"""
This script recursively scans a given path and applies a cleaning 'action' 
to matching files and folders. By default files and folders matching the 
specified (.endswith) patterns are deleted. Alternatively, _quoted_ glob
patterns can used with the '-g' option.

By design, the script lists targets and asks permission before applying 
cleaning actions. It should be easy to extend this script with further 
cleaning actions and more intelligent pattern matching techniques.

The getch (single key confirmation) functionality comes courtesy of 
http://code.activestate.com/recipes/134892/

To use it, place the script in your path and call it something like 'clean':

    Usage: clean [options] patterns
        
            deletes files/folder patterns:
                clean .svn .pyc
                clean -p /tmp/folder .svn .csv .bzr .pyc
                clean -g "*.pyc"
                clean -ng "*.py"
    
            converts line endings from windows to unix:
                clean -e .py
                clean -e -p /tmp/folder .py

    Options:
      -h, --help            show this help message and exit
      -p PATH, --path=PATH  set path
      -n, --negated         clean everything except specified patterns
      -e, --endings         clean line endings
      -v, --verbose         

"""
from __future__ import print_function
import os, sys, shutil
from fnmatch import fnmatch
from optparse import OptionParser
from os.path import join, isdir, isfile


# to enable single-character confirmation of choices
try:
    import sys, tty, termios
    def getch(txt):
        print(txt, end=' ')
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
except ImportError:
    import msvcrt
    def getch(txt):
        print(txt, end=' ')
        return msvcrt.getch()

# -----------------------------------------------------
# main class

class Cleaner(object):
    """recursively cleans patterns of files/directories
    """
    def __init__(self, path, patterns):
        self.path = path
        self.patterns = patterns
        self.matchers = {
            # a matcher is a boolean function which takes a string and tries 
            # to match it against any one of the specified patterns, 
            # returning False otherwise
            'endswith': lambda s: any(s.endswith(p) for p in patterns), 
            'glob': lambda s: any(fnmatch(s, p) for p in patterns),
        }
        self.actions = {
            # action: (path_operating_func, matcher)
            'endswith_delete': (self.delete, 'endswith'),
            'glob_delete': (self.delete, 'glob'),
            'convert': (self.clean_endings, 'endswith'),
        }
        self.targets = []
        self.cum_size = 0.0

    def __repr__(self):
        return "<Cleaner: path:%s , patterns:%s>" % (
            self.path, self.patterns)

    def _apply(self, func, confirm=False):
        """applies a function to each target path
        """
        i = 0
        desc = func.__doc__.strip()
        for target in self.targets:
            if confirm:
                question = "\n%s '%s' (y/n/q)? " % (desc, target)
                answer = getch(question)
                if answer in ['y', 'Y']:
                    func(target)
                    i += 1
                elif answer in ['q']: #i.e. quit
                    break
                else:
                    continue
            else:
                func(target)
                i += 1
        if i:
            self.log("Applied '%s' to %s items (%sK)" % (
                desc, i, int(round(self.cum_size/1024.0, 0))))
        else:
            self.log('No action taken')

    @staticmethod
    def _onerror(func, path, exc_info): 
        """ Error handler for shutil.rmtree.

            If the error is due to an access error (read only file)
            it attempts to add write permission and then retries.

            If the error is for another reason it re-raises the error.

            Usage : ``shutil.rmtree(path, onerror=onerror)``
            
            original code by Michael Foord
            bug fix suggested by Kun Zhang

        """
        import stat
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    def log(self, txt):
        print('\n' + txt)

    def do(self, action, negate=False):
        """finds pattern and approves action on results
        """
        func, matcher = self.actions[action]
        if not negate:
            show = lambda p: p if self.matchers[matcher](p) else None
        else:
            show = lambda p: p if not self.matchers[matcher](p) else None
        
        results = self.walk(self.path, show)
        if results:
            question = "%s item(s) found. Apply '%s' to all (y/n/c)? " % (
                len(results), func.__doc__.strip())
            answer = getch(question)
            self.targets = results
            if answer in ['y','Y']:
                self._apply(func)
            elif answer in ['c', 'C']:
                self._apply(func, confirm=True)
            else:
                self.log("Action cancelled.")
        else:
            self.log("No results.")

    def walk(self, path, func, log=True):
        """walk path recursively collecting results of function application
        """
        results = []
        def visit(root, target, prefix):
            for i in target:
                item = join(root, i)
                obj = func(item)
                if obj:
                    results.append(obj)
                    self.cum_size += os.path.getsize(obj)
                    if log: 
                        print(prefix, obj)
        for root, dirs, files in os.walk(path):
            visit(root, dirs, ' +-->')
            visit(root, files,' |-->')
        return results

    def delete(self, path):
        """delete path
        """
        if isfile(path):
            os.remove(path)
        if isdir(path):
            shutil.rmtree(path, onerror=self._onerror)

    def clean_endings(self, path):
        """convert windows endings to unix endings
        """
        with file(path) as old:
            lines = old.readlines()
        string = "".join(l.rstrip()+'\n' for l in lines)
        with file(path, 'w') as new: 
            new.write(string)

    @classmethod
    def cmdline(cls):
        usage = """usage: %prog [options] patterns
        
        deletes files/folder patterns:
            %prog .svn .pyc
            %prog -p /tmp/folder .svn .csv .bzr .pyc
            %prog -g "*.pyc"
            %prog -gn "*.py"

        converts line endings from windows to unix:
            %prog -e .py
            %prog -e -p /tmp/folder .py"""

        parser = OptionParser(usage)
        parser.add_option("-p", "--path", 
                          dest="path", help="set path")
        
        parser.add_option("-n", "--negated",
                         action="store_true", dest="negated", 
                         help="clean everything except specified patterns")
    
        parser.add_option("-e", "--endings", 
                          action="store_true", dest="endings",
                          help="clean line endings")
        
        parser.add_option("-g", "--glob", 
                          action="store_true", dest="glob",
                          help="clean with glob patterns")
    
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose")

        (options, patterns) = parser.parse_args()

        if len(patterns) == 0:
            parser.error("incorrect number of arguments")

        if not options.path:
            options.path = '.'
    
        if options.verbose:
            print('options:', options)
            print('finding patterns: %s in %s' % (patterns, options.path))
        
        cleaner = cls(options.path, patterns)
    
        # convert line endings from windows to unix
        if options.endings and options.negated:
            cleaner.do('convert', negate=True)
        elif options.endings:
            cleaner.do('convert', negate=True)
        
        # glob delete
        elif options.negated and options.glob:
            cleaner.do('glob_delete', negate=True)
        elif options.glob:
            cleaner.do('glob_delete')

        # endswith delete (default)
        elif options.negated:
            cleaner.do('endswith_delete', negate=True)
        else:
            cleaner.do('endswith_delete')

if __name__ == '__main__':
    Cleaner.cmdline()
