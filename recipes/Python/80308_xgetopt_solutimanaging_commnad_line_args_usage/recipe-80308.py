#!/usr/bin/env python
#
# xgetopt.py
#
# Copyright (c) 2001 Alan Eldridge. All rights reserved.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the "Artistic License" which is
# distributed with the software in the file LICENSE.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Artistic
# License for more details.
#
# Alan Eldridge 2001-09-15 alane@wwweasel.geeksrus.net
#
# $Id: xgetopt.py,v 1.13 2001/10/14 04:57:58 alane Exp $
#
# 2001-09-15 alane@wwweasel.geeksrus.net
#

import os
import sys
import string
import getopt

import word_wrap

class parser:
    """Simple wrapper around getopt to specify short and long options
    together by function, to create a usage message from the options.
    """
    __usage_lwid=30
    __usage_rwid=40
    __usage_width=70

    def __init__(self):
        """Set up empty tables for parser."""
        self.__app = None
        self.__args = None
        self.__note = None
        self.__s = []   # short opts for getopt
        self.__l = []   # long opts for getopt
        self.__olist = []       # list of opt def'ns
        self.__odict = {}       # opt def'ns indexed by opt
        self.__usage = None     # cached option help message

    def set_app(self, app):
        self.__app = app

    def set_args(self, args):
        self.__args = args

    def set_note(self, note):
        self.__note = note

    def add_opt(self, opt, long, arg, key, usage, multi=0):
        """Add a new option to the parser's tables.

        opt     => short option, e.g., '-s', *not* 's' or 's:'.
        long    => long option, e.g., '--spam', *not* '--spam='.
        arg     => descriptive name for arg to option, if it has an
                   an arg, e.g., 'how-much-spam'.
        key     => a unique key to identify this option; see
                   xgetopt.getopt().
        usage   => usage text for this option; may contain references
                   to members of the opt_info dictionary such as %(opt)s
                   and %(arg)s; '\n' is a paragraph separator.
        multi   => if true, multiple values for the option are distinct;
                   if false, only the last value is significant. See
                   xgetopt.getopt() for detail.
        """
        self.__usage = None
        # Build opt def'n dict
        opt_info = {}
        opt_info['opt'] = opt
        opt_info['long'] = long
        opt_info['arg'] = arg
        opt_info['key'] = key
        opt_info['usage'] = usage
        opt_info['multi'] = multi
        # Setup for getopt
        # Make index entries
        if opt:
            self.__odict[opt] = opt_info
            if arg:
                opt = opt + ':'
            self.__s.append(opt[1:])
        if long:
            self.__odict[long] = opt_info
            if arg:
                long = long + '='
            self.__l.append(long[0:])
        # Split usage into paragraphs and substitute vars.
        # This is gonna die a horrible death if the string
        # has bad variable substitutions in it.
        if usage:
            opt_info['usage'] = string.split(usage % opt_info, '\n\n')
        # Add to list of options
        self.__olist.append(opt_info)
        return opt_info

    def getopt(self, args, app_opts = None):
        """Parse string 'args' using saved option info.

        Returns a 3-tuple (opts, args, app_opts). Opts and args
        are the conventional values returned by getopt.getopt().

        App_opts is a dictionary mapping the 'key' given to add_opt()
        for each option to the value present on the command line.

        1. If the app_opts dictionary is passed in, this gives the
        default values for options for the application.

        2. Options not present in a passed-in app_opts, and not present
        on the command line have a mapped value of None.

        2. Options that have the 'multi' flag set have a mapped value
        of a list containing all values for the option that were given
        on the command line, in the order they were given.

        """
        # set up dict for caller
        if app_opts is None:
            app_opts = {}
        for oinfo in self.__olist:
            if not app_opts.has_key(oinfo['key']):
                app_opts[oinfo['key']] = None

        # Do the getopt thing
        opts, args = getopt.getopt(args,
                                   string.join(self.__s, ''),
                                   string.join(self.__l, ' '))

        # now fill in caller dict
        for k, v in opts:
            app_key = self.__odict[k]['key']
            app_multi = self.__odict[k]['multi']
            if app_multi:
                if not app_opts[app_key]:
                    app_opts[app_key] = []
                app_opts[app_key].append(v)
            else:
                app_opts[app_key] = v

        # return 3-tuple to caller
        return opts, args, app_opts

    def usage_msg(self):
        """Generate a help message using saved option info."""
        if self.__usage:
            return self.__usage
        app = self.__app
        if not app:
            app = sys.argv[0].split(os.sep)[-1]
        str = 'Usage: ' + app
        if len(self.__olist):
            str = str + ' [options]'
        if self.__args:
            str = str + ' ' + self.__args
        self.__usage = map(lambda s: s + '\n', str.split('\n'))
        if len(self.__olist):
            self.__usage = self.__usage + ['\n', 'Options:\n']
        # Loop over options
        for oinfo in self.__olist:
            lside = rside = ''
            # Left side is -x,--xthing xarg
            if oinfo['opt']:
                lside = lside + oinfo['opt']
            if oinfo['long']:
                if oinfo['opt']:
                    lside = lside + ','
                lside = lside + oinfo['long']
            if oinfo['arg']:
                lside = lside + ' ' + oinfo['arg']
            lside = [ string.ljust(lside, self.__usage_lwid) ]
            # Right side is usage, word wrapped to fit
            rside = word_wrap.wrap_list(oinfo['usage'], self.__usage_rwid)
            # Pad out extra blank lines on left side
            for i in range(len(rside) - 1):
                lside.append(string.ljust('', self.__usage_lwid))
            # Tack 'em together
            self.__usage = self.__usage +  map(lambda l, r: l + r + '\n',
                                               lside, rside)
        if self.__note:
            self.__usage.append('\n')
            tmp = map(lambda s: s + '\n',
                      word_wrap.wrap_str(self.__note, self.__usage_width, '\n\n'))
            self.__usage = self.__usage + tmp
        return self.__usage

    def usage(self, rc):
        map(sys.stdout.write, self.usage_msg())
        sys.exit(rc)
 
#
#EOF
##
       self.__usage = self.__usage + tmp
