#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original copyright, license and disclaimer are further below.

# This is an enhanced version of the recipe originally posted at
# <http://code.activestate.com/recipes/546532/>
'''
   This %(_argv0)s script is a postprocessor for Python source code
   checkers PyChecker <http://pychecker.sourceforge.net>, PyFlakes
   <http://pypi.python.org/pypi/pyflakes>, PyCodeStyle (formerly Pep8)
   <http://pypi.python.org/pypi/pycodestyle> and/or the "Meager" McCabe
   code complexity tool <http://nedbatchelder.com/files/codepaths0.py>).

   Usage: %(_argv0)s  [-h|-help  [-no-OKd|-no]  [-debug|-Debug]
           [-Checker]  [-Flakes]  [-McCabe]  [-Style|-Pep8]  [-3]
           [-blacklist <mods>]  [-cmd <path>]  [-EW]  [-PATH]
           [-raiser]  [-recursive]  [-Tb]  [-v|--versions]  [-which]
           [-Xpy]  [--|---]  [<options>]  <file_or_dir> ...

   where <options> are PyChecker, PyFlakes or PyCodeStyle (Pep8)
   options* and <file_or_dir> and all following command line arguments
   are Python source file names or directory names.

   This %(_argv0)s script first runs PyChecker, PyFlakes, McCabe and/or
   PyCodeStyle (Pep8) on <file_or_dir> and all subsequent arguments
   using command(s) %(_Cmds)s.

   Next, it splits the output from PyChecker, PyFlakes, McCabe and
   PyCodeStyle (Pep8) into two sets of warning messages, OK'd and
   regular messages.

   A warning message is considered OK'd if the Python source line
   causing the warning message ends with a comment starting with
   %(_OKs)s**).

   OK'd warning messages can be suppressed entirely by using option
   -no or -no-OKd.  Only non-OKd warnings are printed in that case.

   However, certain errors like PyChecker INTERNAL ERROR ... (often
   followed by a traceback) can't be OK'd, can't be suppressed and
   are always printed without the PyChecker traceback.  Use option
   -Tb to show the traceback.

   To run PyChecker only, use option -C or -Checker if the command
   '%(_CmdC)s' is in your search PATH.  Otherwise use option -cmd
   to specify the PyChecker path.

   To run PyFlakes only, use option -F or -Flakes if the command
   '%(_CmdF)s' is in your search PATH.  Otherwise use option -cmd
   to specify the PyFlakes path.

   To run McCabe only, use option -M or -McCabe if the command
   '%(_CmdM)s' is in your search PATH.  Otherwise use option -cmd to
   specify the McCabe path.

   To run PyCodeStyle only, use option -Style or -Pep8 if command
   '%(_CmdP)s' is in your search PATH.  Otherwise use option -cmd
   to specify the PyCodeStyle (Pep8) path.

   Use option -3 to run PyChecker3, PyFlakes3, McCabe3 and
   PyCodeStyle3, the Python 3+ versions of the checkers even
   if this %(_argv0)s script is invoked with Python 2.

   By default, warnings from some modules "%(_blacklist)s"
   are ignored, rather OK'd implicitly.  To ignore additional
   modules use option -blacklist <mods> where <mods> is a string
   of comma-separated module names.

   Also, Python file names ending with '%(_Xpy)s' are ignored entirely.
   Use option -Xpy to check and process such files.

   Option -debug or -Debug produces additional %(_argv0)s output.

   Option -EW allows these PyCodeStyle (Pep8) errors to be OK'd:
    %(_EWs)s

   in addition to these PyCodeStyle (Pep8) errors always OK'd:
    %(_OKdEs)s

   By default, run PyChecker, PyFlakes, McCabe and PyCodeStyle (Pep8)
   provided commands 'pyflakes', 'pychecker', 'mccabe' and 'pycodestyle'
   are in your search PATH.  Use option -PATH to append the directory
   containing this very script to the search PATH.

   Option -raiser shows the traceback or other exception details.

   Option -recursive causes sub-directory to be visited.

   Option -versions prints the version of this script, PyChecker,
   PyFlakes, McCabe, PyCodeStyle (Pep8) and Python if found in PATH.

   Option -which prints the fully qualified path of this script.

   Tested with PyChecker 0.8.17, 0.8.18 and 0.8.19, PyFlakes 0.7.3,
   1.0.0, 1.2.3 and 1.4.0, McCabe 2008.3, Pep8 1.4.6, 1.6.2, 1.7.0
   and PyCodeStyle (formerly Pep8) 2.2.0 using 32- and/or 64-bit
   Python 2.3.4, 2.4.4, 2.5.2, 2.6.4, 2.7.1, 2.7.5, 2.7.9, 2.7.10
   or 2.7.13 on CentOS 4.6, RHEL 3u7, Ubuntu 10.10, MacOS X 10.4.11
   (Tiger, Intel), MacOS X 10.9.1 (Mavericks), MacOS X 10.10.5
   (Yosemite), MacOS X 10.11.5 (El Capitan), MacOS 10.12.2 (Sierra),
   Solaris 10, Windows 7, Windows XP SP3 and Windows Server 2003.

   Tested with Flake8 3.2.1 (PyCodeStyle 2.2.0, PyFlakes 1.3.0 and
   McCabe 0.5.3) using 64-bit Python 3.6.0 on MacOS 10.12.2 (Sierra).

___
 *) Beware of overlapping PyChecker option names and abbreviations
    with options for this script.  PyChecker options -d, --debug,
    -Q and --quiet are honored as additional options of this script.

**) %(_OKs)s
    are all upper case and there must be at least one space between
    %(_OKs)s
    and the end of the source line.
'''

__all__     = ('Processor', 'main')
__version__ =  '17.01.10'

import os
import sys

# defaults
_and       = '; '  # ' && '
_argv0     =  os.path.basename(sys.argv[0])
_blacklist = ('[system path]/', '/boto/')
_Debug     =  False  # print debug info
_EW        =  False  # additional OK'd errors/warnings
_EWs       = {  # additional PyCodeStyle (Pep8) errors OK'd
              'E101': 'indentation contains mixed spaces and tabs',
              'E131': 'continuation line unaligned for hanging indent',
              'E265': "block comment should start with '# '",
              'E266': "too many leading '#' for block comment",
              'E305': 'expected 2 blank lines after class or function definition',
              'W191': 'indentation contains tabs',
              'W503': 'line break before binary operator'}
_INTERROR  =  None   # INTERNAL ERROR never OK'd
_NL        = '\n'
_None      = 'None'  # line from pychecker
_OKd       =  True   # print OK'd warnings
# PyCodeStyle (Pep8) option --ignore=E111,E121,E122,... doesn't work in Pep8 1.4.6
_OKdEs     = {  # PyCodeStyle (Pep8) error message ignored and OK'd with  # PEP8 OK'd
#             'E111': 'indentation is not a multiple of four',  # PYCHOK expected
              'E121': 'continuation line indentation is not a multiple of four',
              'E122': 'continuation line missing indentation or outdented',
              'E126': 'continuation line over-indented for hanging indent',
              'E127': 'continuation line over-indented for visual indent',
              'E128': 'continuation line under-indented for visual indent',
              'E201': "whitespace after '",  # '(', '[', ...
              'E203': "whitespace before '",  # ',', ':', ...
              'E211': "whitespace before '",  # '('
              'E221': 'multiple spaces before operator',
              'E222': 'multiple spaces after operator',
              'E225': 'missing whitespace around operator',
              'E226': 'missing whitespace around arithmetic operator',
              'E231': "missing whitespace after '",  # ','
              'E241': "multiple spaces after '",  # ',', ':', ...
              'E251': 'unexpected spaces around keyword / parameter equals',
              'E271': 'multiple spaces after keyword',
              'E272': 'multiple spaces before keyword',
              'E402': 'module level import not at top of file',
              'E501': 'line too long ('}  # 81 > 79 characters)
_OKs       = ('# PYCHOK ', '# PYCHECKER ',
              '# MCCABE ', '# PEP8 ', '# PYFLAKE ',
              '# noqa', '# NOQA')  # Flake8
_Out       =  sys.stdout  # output file
_PATH      =  os.environ.get('PATH', '').split(os.pathsep)
_Py3       =  sys.version_info[0] == 3
_Raiser    =  False
_Recursive =  False
_Warnings  = 'Warnings...'  # line from pychecker
_X3        =  False  # run Python 3+ checkers
_Xtb       =  True  # exclude traceback lines
_Xpy       = 'X.py'  # ignore these modules
_xtensions = ('',)

if sys.platform.startswith('win'):
    _blacklist += tuple(p.replace('/', '\\') for p in _blacklist if '/' in p)
    _xtensions += ('.bat', '.BAT', '.exe', '.EXE')

if _Py3:
    _CmdC = 'pychecker3 --limit 0 --stdlib'  # XXX no PyChecker
    _CmdF = 'pyflakes3'  # PyFlakes 1.3.0 (from Flake8)
    _CmdM = 'mccabe3 --min 13'  # McCabe 0.5.3
    _CmdP = 'pycodestyle3 --max-line-length=99'  # PyCodeStyle 2.2.0+
    _Cmds = 'flake83 --max-line-length=99'  # Flake8 3.2.1 Python 3+
else:
    _CmdC = 'pychecker --limit 0 --stdlib'  # PyChecker 0.8.17+
    _CmdF = 'pyflakes'  # PyFlakes 0.4.0+
    _CmdM = 'mccabe --min 13'  # McCabe
    _CmdP = 'pycodestyle --max-line-length=99'  # --format='%(path)s:%(row)d: %(code)s %(text)s'  # Pep8 1.4.6+
    _Cmds = _and.join([_CmdC, _CmdF, _CmdM, _CmdP])

try:
    from subprocess import Popen, PIPE

    # <http://docs.python.org/library/subprocess.html#replacing-os-popen>
    # <http://bugs.python.org/issue4194> for subprocess.Popen vs os.popen
    def _popen(cmd):  # return stdout
        return Popen(cmd, shell=True, bufsize=-1, stdout=PIPE).stdout

except ImportError:  # no subprocess
    def _popen(cmd):  # return stdout  # PYCHOK expected
        return os.popen(cmd, 'r')  # bufsize=-1 by default


def b2s(b):
    '''Decode bytes to str/unicode.
    '''
    # XXX alternative would be to use subprocess.Popen keyword arguments
    # universal_newlines=True, encoding=..., errors=... but those apply
    # only to later versions of the subprocess.Popen constructor.  See
    # <https://docs.python.org/3/library/subprocess.html> at 17.5.1.2.
    if _Py3 and isinstance(b, bytes):
        b = b.decode()  # encoding='utf-8', errors='strict'
    return b


def bits():
    '''Return 32- or 64-bit size of this Python.
    '''
    try:
        import platform
        return int(platform.architecture()[0][:2])
    except (AttributeError, ImportError, ValueError):
        import struct
        return struct.calcsize('P') << 3


def plural(n, unit):
    '''Format a plural string.
    '''
    s = 's' if n != 1 else ''
    return '%s %s%s' % (n or 'no', unit, s)


def quoted(text):
    '''Enquote text if needed.
    '''
    if len(text.split()) != 1:
        return '"%s"' % (text,)
    else:
        return text


def which(exe):
    '''Return full path of an executable.
    '''
    for d in _PATH:
        for x in _xtensions:
            p = quoted(os.path.join(d, exe) + x)
            if os.access(p, os.X_OK):
                return p
    raise OSError('no such executable: %s' % (exe,))


class Processor(object):
    '''Processor to handle suppression of OK'd PyChecker, PyFlakes
       and PyCodeStyle (Pep8) warning messages, marked as such at
       the end of the Python source code line.
    '''
    _code = []  # source code lines
    _dirs = ()  # source file directories
    _name = ''  # source file name

    _cmds  = ()      # commands to run
    _debug = _Debug  # print debug output
    _OKd   = _OKd    # print OK'd warnings
    _out   = _Out    # output file, None for quiet
    _title = True    # print module title
    _x3    = _X3     # run Python 3+ checkers

    def __init__(self, cmds, OKd=_OKd, debug=_Debug, out=_Out, x3=False):
        self._debug = debug
        self._OKd   = OKd
        self._out   = out
        self._cmds  = []
        for c in cmds.split(_and):
            c = c.split()
            try:
                x = c[0]  # checker
                if x3 and not x.endswith('3'):
                    x += '3'
                c[0] = x = which(x)
                self._cmds.append(' '.join(c))
                if 'pychecker' in x.lower():
                    self._title = False  # don't print
                self._x3 = x3
            except OSError:
                self.printf('%s warning: %s', _argv0, sys.exc_info()[1])

    def allist(self, name):
        '''Check that the objects named in the
           __all__ list do exist in the module.
        '''
        self.debugf("running '%s %s' ...", 'allist', name)
        n, w = 0, []
        try:
            m = __import__(name[:-3])
        except ImportError:
            m = None
        for a in getattr(m, '__all__', []):
            if not hasattr(m, a):
                if not n:  # get __all__ line number, once
                    if name != self._name:
                        self.get(name)
                    for i, t in enumerate(self._code):
                        if t.startswith('__all__'):
                            n = i + 1
                            break
                w.append('%s:%d: no %s object %r in module %r' %
                         (name, n, '__all__', a, m.__name__))
        self.debugf('%s of %r output', plural(len(w), 'line'), 'allist')
        return tuple(w)

    def debugf(self, fmt, *args):
        '''Debug print.
        '''
        if self._debug:
            self.printf('Debug: %s ' + fmt, _argv0, *args)

    def dirs(self, *args):
        '''Get all source directories.
        '''
        ds = []
        for f in args:
            if f.startswith('-'):
                # honored PyChecker options
                if f in ('--quiet', '-Q'):
                    self._out = None
                elif f in ('--debug', '-d'):
                    self._debug = True
            else:
                n = max(f.count(os.path.sep), 1)
                d = os.path.realpath(f)
                while d and n > 0:
                    n -= 1
                    d  = os.path.dirname(d)
                    if d and d not in ds:
                        ds.append(d)
        ds.append('.')
        for d in sys.path:
            if os.path.isdir(d) and d not in ds:
                ds.append(d)
        self._dirs = tuple(ds)

    def get(self, name):
        '''Get source code for a given file.
        '''
        self._code = []
        self._name = name
        if name.lower().endswith('.py'):
            self.debugf('looking for file: %s', name)
            if os.path.isabs(name):
                # XXX assert(os.path.join('', name) == name)
                ds = ('',)
            else:
                ds = self._dirs
            for d in ds:  # find file
                try:
                    t = os.path.join(d, name)
                    f = open(t, 'r')
                    s = f.readlines()
                    f.close()
                    self._code = s
                    self.debugf('found file: %s (%s)', t, plural(len(s), 'line'))
                    break
                except (IOError, OSError, EOFError):
                    pass
            else:
                self.debugf('file not found: %s', name)

    def isOK(self, name, line, Error=''):
        '''Check whether source line is marked.
        '''
        # never OK PyChecker INTERNAL ERRORs,
        # since those typically stop checking
        if Error.startswith(' INTERNAL ERROR --'):
            return _INTERROR
        # check module/file name against blacklist
        for p in _blacklist:
            if p in name:  # OK, black listed
                return '# PYCHOK blacklist %s' % (p,)
        # get source code
        if name != self._name:
            self.get(name)
        try:  # get source line
            n = int(line) - 1
            while True:
                s = b2s(self._code[n]).rstrip()
                for OK in _OKs:
                    p = s.find(OK)
                    if p > 0:  # line OK'd
                        return s[p:]
                # handle continuation lines
                if s.endswith('\\'):
                    n += 1
                else:
                    break
            # not OK'd, check Pep8 Errors to ignore
            e = Error.split(' ', 2)
            if len(e) > 2 and e[2].startswith(_OKdEs.get(e[1], ' ')):
                return "# PEP8 OK'd"
        except (ValueError, IndexError):
            self.debugf('no line %s in file: %s', line, self._name)
        return ''  # not OK'd, not black listed, not found, etc.

    def printf(self, fmt, *args):
        '''Formatted print.
        '''
        if self._out:
            if args:
                self._out.write(fmt % args)
            else:
                self._out.write(fmt)
            self._out.write(_NL)

    def process(self, output):
        '''Split PyChecker/-Flakes output into
           OK'd and other warning messages.
        '''
        if self._OKd:
            self.printf('Splitting...')
        if self._debug:
            self.debugf('source directories...')
            for t in enumerate(self._dirs):
                self.printf('%5d: %r', *t)

        mt = []  # list of 2-tuples (message, OK'd)
        e = False  # or a split INTERNAL ERROR line
        n = t = 0  # number of non-OK'd, total warnings
        for m in output:  # process each warning line
            m = b2s(m).rstrip()
            if m:  # only non-blank lines
                if e and _Xtb:  # after INTERNAL ERROR
                    s = m.lstrip()
                    if len(s) < len(m):  # traceback line
                        e[2] = ' ' + s  # save last one
                        continue
                    # build another INTERNAL ERROR
                    # from the last trackback line,
                    # usually the exception raised
                    mt.append((':'.join(e), _INTERROR))
                    e = False
                # split and process warning line
                ok, s = '', m.split(':', 2)
                if len(s) > 2:  # file name, line number, rest
                    if not s[1].isdigit():
                        self.debugf('no line number: %r', m)
                        continue
                    ok = self.isOK(*s)
                    if not ok:
                        n += 1  # non-OK'd
                        if ok is _INTERROR:
                            e = s
                    t += 1  # total
                elif _EW or m in (_Warnings, _None):
                    continue
                mt.append((m, ok))

        if self._out:
            if self._OKd:  # print OK'd warnings
                self.printf("%sLines OK'd...", _NL)
                m = [m + ' - ' + ok for m, ok in mt if ok]  # PYCHOK expected
                self.printf(_NL.join(m) or _None)

            # print other warnings (and lines)
            m = [m for m, ok in mt if not ok]  # PYCHOK expected
            if m:  # print always
                self.printf(_NL + _Warnings)
                self.printf(_NL.join(m))
            elif t > 1 and self._OKd:
                self.printf(_NL + _Warnings)
                self.printf("%s, all %s OK'd", _None, t)

        return n  # number of non-OK'd warnings

    def run(self, cmd, arg):
        '''Run command and return output.
        '''
        c = ' '.join([cmd, quoted(arg)])
        self.dirs(arg)
        self.debugf('running %r ...', c)
        m = _popen(c).readlines()
        self.debugf('%s of %r output', plural(len(m), 'line'), cmd)
        return tuple(m)  # output as lines

    def versions(self):
        v = sys.version.split()[0]
        v = '(%s-bit Python %s)' % (bits(), v)
        t = [(_argv0, __version__, v)]
        for c in self._cmds:
            c = c.split()[0]
            try:
                v = b2s(_popen(c + ' --version').readline())
            except OSError:
                v = ''
            t.append((c, v.strip() or 'n/a'))
        if self._x3 and not _Py3:
            try:
                v = b2s(_popen('python3' + ' --version').readline())
            except OSError:
                v = ''
            t.append((v.strip() or 'n/a',))
        return [' '.join(v) for v in t]  # PYCHOK expected

    def warnings(self, arg):
        '''Return number of non-OK'd warnings.
        '''
        if self._title:
            m = os.path.splitext(os.path.basename(arg))[0]
            self.printf('Processing module %s (%s) ...', m, arg)
        w = ()
        for c in self._cmds:
            w += self.run(c, arg)
        w += self.allist(arg)
        n = self.process(w)
        self.printf('%s%s in %s', _NL, plural(n, 'error'), arg)
        return n


def main(args, cmds=_Cmds, OKd=_OKd, out=_Out, debug=_Debug,
               recursive=_Recursive, x3=_X3):
    '''Get a postprocessor, run the commands on the
       given arguments, split the output and return
       the number of non-OK'd warnings.
    '''
    m = n = 0
    p = Processor(cmds, OKd, debug, out=out, x3=x3)
    while args:
        arg = args.pop(0)
        if os.path.isdir(arg):
            for d, ds, fs in os.walk(arg):
                for f in fs:
                    if _Xpy and f.endswith(_Xpy):
                        pass  # exclude
                    elif f.endswith('.py'):
                        f  = os.path.join(d, f)
                        n += p.warnings(f)
                        m += 1
                if recursive:
                    args.extend(ds)
        else:
            n += p.warnings(arg)
            m += 1
    if m != 1:
        p.printf('%s%s total in %s', _NL, plural(n, 'error'), plural(m, 'module'))
    return n  # number of non-OK'd warnings


if __name__ == '__main__':

    def usage(status):
        global _blacklist, _CmdC, _CmdF, _CmdM, _CmdP, _EWs, _OKdEs, _OKs
        _blacklist = ', '.join(_blacklist)
        _CmdC = _CmdC.split()[0]
        _CmdF = _CmdF.split()[0]
        _CmdM = _CmdM.split()[0]
        _CmdP = _CmdP.split()[0]
        _EWs = '\n    '.join('%s: %s' % _ for _ in sorted(_EWs.items()))
        _OKdEs = '\n    '.join('%s: %s' % _ for _ in sorted(_OKdEs.items()))
        _OKs = '.., '.join(_OKs)
        print(__doc__ % globals())
        sys.exit(status)

    try:
        args = sys.argv[1:]
        if not args:
            usage(1)
        while args and args[0].startswith('-'):
            opt = args.pop(0)
            n   = len(opt)
            if opt in ('--', '---'):
                break
            elif opt == '-3':
                _X3 = True
            elif '-blacklist'.startswith(opt) and n > 2 and args:
                _blacklist += tuple(args.pop(0).split(','))
            elif '-Checker'.startswith(opt) and n > 1:
                _Cmds = _CmdC  # PyChecker only
            elif '-cmd'.startswith(opt) and n > 3 and args:
                _Cmds = args.pop(0)
            elif '-debug'.startswith(opt.lower()) and n > 1:
                _Debug = True  # print debug output
            elif '-Flakes'.startswith(opt) and n > 1:
                _Cmds = _CmdF  # PyFlakes only
            elif ('-help'.startswith(opt)  and n > 1) or \
                 ('--help'.startswith(opt) and n > 2):
                usage(0)
            elif '-McCabe'.startswith(opt) and n > 1:
                _Cmds = _CmdM  # McCabe only
            elif '-no-OKd'.startswith(opt) and n > 2:
                _OKd = False  # don't print OK'd warnings
            elif '-PATH'.startswith(opt) and n > 2:
                _PATH.append(os.path.abspath(os.path.dirname(__file__)))
            elif ('-Pep8'.startswith(opt) and n > 1) or \
                 ('-Style'.startswith(opt) and n > 1):
                _Cmds = _CmdP  # PyCodeStyle (Pep8) only
            elif '-raiser'.startswith(opt) and n > 2:
                _Raiser = True
            elif '-recursive'.startswith(opt) and n > 3:
                _Recursive = True
            elif '-Tb'.startswith(opt) and n > 2:
                _Xtb = False
            elif ('-versions'.startswith(opt)  and n > 1) or \
                 ('--versions'.startswith(opt) and n > 2):
                p = Processor(cmds=_Cmds, out=None, x3=_X3)
                print(', '.join(p.versions()))
                sys.exit(0)
            elif '-which'.startswith(opt) and n > 1:
                print('%s which %s' % (_argv0, which(_argv0)))
                sys.exit(0)
            elif '-Xpy'.startswith(opt) and n > 2:
                _Xpy = ''
            elif '-EW' == opt:
                _EW = True
                _OKdEs.update(_EWs)  # extend  # PEP8 OK'd dict
            else:
                raise NameError('invalid option: %s' % (opt,))

        ex = min(5, main(args, cmds=_Cmds,
                                OKd=_OKd,
                              debug=_Debug,
                          recursive=_Recursive,
                                 x3=_X3))

    except KeyboardInterrupt:  # PYCHOK expected
        sys.stdout.write('%s%s: ^C%s' % (_NL, _argv0, _NL))
        ex = 9  # ^C
    except SystemExit:  # PYCHOK expected
        ex = 8  # early exit
    except Exception:
        if _Raiser:
            raise
        t = _argv0, sys.exc_info()[1], _NL
        sys.stderr.write('%s error: %s%s' % t)
        ex = 1  # exception

    sys.exit(ex)


# License file from an earlier version of this source file follows:

# --------------------------------------------------------------------
#       Copyright (c) 2002-2008 -- ProphICy Semiconductor, Inc.
#                        All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of ProphICy Semiconductor, Inc. nor the names
#   of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------
