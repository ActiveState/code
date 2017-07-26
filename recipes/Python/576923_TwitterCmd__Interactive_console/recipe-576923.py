#!/usr/bin/env python

""" TwitterCmd - Interactive, console prompt to twitter
written on top of the python-twitter API.

A lot of credit to DeWitt Clinton and his team of
developers for the excellent 'python-twitter' API on
top of which, this program is written on.

Author: Anand B Pillai ('pythonhacker')
License: BSD License

"""

from twitter import Api
from cmd import Cmd
import sys, os
import re
import urllib2
import optparse
import time
import glob
import cPickle
import subprocess

__version__ = 0.3
__author__ = 'Anand B Pillai'
__lastmodified__ = "Thu Oct  8 14:39:24 IST 2009"
__modifications__ = """This version gets session save feature
and ability to enter Python prompt from TwitterCmd and back
while keeping state same across both. Basically you get the
simplicity of TwitterCmd plus the power of python-twitter
in one go!

Oct 8 - Bug in api attribute fixed, loading it fresh always.
        Reduced stuff printed in inspecting timeline & user.
"""

LOADER="""
from twittercmd import *
from twitter import Api
import cPickle, urllib2
obj=cPickle.load(open('%s', 'rb'))
if obj.username:
    obj.api=Api(obj.username)
else:
    obj.api=Api()
g=globals()
g.update(obj.__dict__)
"""

INTRO="""Welcome to TwitterCmd, a command line interface to twitter,
written in Python. TwitterCmd provides a simple, interactive
interface to Twitter with short, easy to remember commands.

For a full set of commands, type "help" on the prompt.
For help for a specific command try "help <cmd>".

Please send comments/bug reports to <abpillai at gmail dot com>                   
or tweet them to the ID 'pythonhacker'.
"""

HELP="""
The following commands are available.

User commands

1. l <user> <passwd> - Set login credentials.
2. u <user>          - Get details of a user.
3. f                 - Get friend's details.
4. fo                - Get followers' details.

Timeline commands

1. pt                - Get public timeline.
2. ut [<user>]       - Get current user timeline
                       (given no arguments), or
                       timeline of given user.
3. ft                - Get all friends' timeline.

Message commands

1. m <msg>           - Post a status message.
2. im <user> <msg>   - Post a direct message to user.
3. r                 - Get replies to messages.
4. dm                - Get all direct messages.

You can also use the 'inspect' or 'i' command to
inspect live objects. The following object types are
supported as argument.

1. s/status          - Inspect current msg status.
2. f/p/friends/peers - Inspect current friends status.
3. t/tl/tline        - Inspect current timeline.
4. u/user            - Inspect current user.

Version 0.2 also adds the power of entering Python
prompt while keeping state intact. To enter Python
prompt use any of 'shell','py' or 'python' commands.

Examples:

# Post a message
Twitter> l user pass
Twitter> m Hey, I love twitter! 

# Get direct messages
Twitter> dm
["'No problem. :-)' => dloss"]

# Get names of all friends
Twitter> f
['dloss', 'gvanrossum', 'MallikaLA', 'BarackObama', 'ShashiTharoor']

# Use Python prompt from TwitterCmd

Twitter> py
Entering Python shell...
>>>
# Inspect objects in shell and use python-twitter
# directly by using the 'api' object.
>>> api
<twitter.Api object at 0x7fb69e6509d0>
# All state of TwitterCmd is available as globals
# in the interpreter...
>>> tline
[<twitter.Status object at 0xe643ad0>, <twitter.Status object at 0xe643d50>]
>>> status
<twitter.Status object at 0x7fb69e643850>
>>> status.text
'Completed session saving and entering Python shell and back from TwitterCmd\
, code will be up in a while, Hooray!'
# Use api just as you would before...!
>>> [s.text for s in api.GetPublicTimeline()]
['tweeting from gravity',...]
# Exit Python prompt
>>> ^D
Exiting Python shell...
Twitter>

To exit a session, type q/quit/exit or Ctrl-D.
"""

class TwitterCmdException(Exception):
    pass

class TwitterCmd(Cmd):
    """ Python command interpreter to Twitter API. Allows a simple
    interactive interface to Twitter to those who prefer twittering
    from their *nix console, while providing the flexibility to
    switch back and forth from Python interactive prompt keeping
    state intact """

    commands = {'m' : 'PostUpdate', 'im': 'PostDirectMessage',
                'ut': 'GetUserTimeline', 'pt': 'GetPublicTimeline',
                'ft': 'GetFriendsTimeline', 'fo': 'GetFollowers',
                'f': 'GetFriends', 'r': 'GetReplies',
                'dm': 'GetDirectMessages', 'u':'GetUser',
                'l': 'SetCredentials'}
    
    prompt = 'Twitter> '
    intro = INTRO
    
    onecmd = lambda self, line: (line==None) and True
    emptyline = lambda self: None
    default = lambda self, line: None

    
    def __init__(self, user='', passwd=''):
        self.api = Api()
        if user and passwd:
            self.api.SetCredentials(user, passwd)
        # Current username
        self.username = user
        # Current command
        self.cmd = ''
        # Current message status
        self.status = None
        # Current timeline
        self.tline = None
        # Current user object
        self.user = None
        # Current friends/followers
        self.peers = None
        # System stuff
        # Python executable
        self.python = sys.executable
        Cmd.__init__(self)
        # Load previous session
        self.load_session()

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['stdin']
        del odict['stdout']
        del odict['api']
        return odict

    def __setstate__(self, dict):
        # Don't update api object...
        try:
            del dict['api']
        except KeyError:
            pass
        self.__dict__.update(dict)
        
    def precmd(self, line):

        line = line.strip()
        if len(line)==0:
            return line
        
        if line.lower() in ('q','quit','exit','eof'):
            print
            self.save_session()
            return None

        if line.lower().startswith('help'):
            self.print_help(line)
            return line

        if line.lower() in ('shell','py','python'):
            # Start Python interpreter with current state
            self.run_wild()
            return line
            
        l = line.split(' ')
        cmd, rest = l[0], l[1:]
        # Inspect objects ?
        if cmd.lower() in ('i','inspect'):
            self.inspect(' '.join(l[1:]).lower())
            return line
        elif cmd not in self.commands:
            print "Command '%s' not understood" % cmd
            return line
        
        self.cmd = cmd.strip()
        try:
            self.action(*rest)
        except IndexError, e:
            print 'Command "%s" requires arguments!' % self.cmd
        except urllib2.HTTPError, e:
            print 'Twitter says:',e
        # Any other exception
        except Exception, e:
            print 'Twitter API says:',e
            
        return line

    def inspect(self, obj_type):
        """ Inspect our objects """

        if obj_type in ('status', 's', 'st'):
            if type(self.status) is list:
                if self.status: print [str(i) for i in self.status]
            else:
                print str(self.status)
        elif obj_type in ('tline','t','tl'):
            if self.tline: print [i.text for i in self.tline]
        elif obj_type in ('user','u'):
            print self.user
        elif obj_type in ('peers','friends','p','f'):
            if self.peers: print [(i.name, i.screen_name) for i in self.peers]       
        else:
            print 'Unknown object type',obj_type
            
    def action(self, *args):
        """ Perform a twitter action """
        
        f = getattr(self.api, self.commands.get(self.cmd, None))
        if self.cmd == 'l':
            if len(args)>=2:
                f(args[0], args[1])
            else:
                f(args[0], '')
            print 'Set login credentials'
        elif self.cmd == 'm':
            # Force IndexError
            x = args[0]
            self.status = f(' '.join(args))
            print repr(self.status)
        elif self.cmd == 'im':
            # Force IndexError
            x = args[0]            
            self.status = f(args[0], ' '.join(args[1:]))
            print repr(self.status)
        elif self.cmd == 'ut':
            self.tline = [f(args[0]) if len(args) else f()][0]
            print [s.text for s in self.tline]
        elif self.cmd == 'pt':
            self.tline = f()
            print [s.text for s in self.tline]
        elif self.cmd == 'ft':
            self.tline = f()
            print [s.text for s in self.tline]
        elif self.cmd == 'r':
            self.status = f()
            print [s.text for s in self.status]            
        elif self.cmd == 'dm':
            self.status = f()
            print [' => '.join(("'" + s.text + "'", s._sender_screen_name)) \
                   for s in self.status]            
        elif self.cmd in ('f','fo'):
            self.peers = f()
            print [s.screen_name for s in self.peers]
        elif self.cmd=='u':
            self.user = f(args[0])
            print self.user.name

    def load_session(self):
        """ Load most recent session from disk, if present """

        fnames = glob.glob(os.path.join(os.path.expanduser('~'),'.twitter_session_*'))
        if len(fnames):
            print 'Loading saved session...'
            try:
                obj = cPickle.load(open(fnames[0], 'rb'))
                self.__setstate__(obj.__dict__)
            except cPickle.UnpicklingError, e:
                print 'Error loading saved session'
        
    def save_session(self):
        """ Save current session to disk """

        fname = os.path.join(os.path.expanduser('~'), '.twitter_session_%d' % int(time.time()))
        try:
            # Remove older sessions
            olds = glob.glob(os.path.join(os.path.expanduser('~'),'.twitter_session_*'))
            cPickle.dump(self, open(fname, 'wb'))
            # Remove older sessions
            for f in olds:
                try:
                    os.remove(f)
                except OSError, e:
                    pass
        except cPickle.PicklingError, e:
            print 'Error saving current session to disk:',e

        return fname

    def run_wild(self):

        session = self.save_session()
        # Create a module that will load the saved session
        loader = LOADER % session
        module = '.twitter_loader.py'
        open(module,'w').write(loader)
        print 'Entering Python shell...'
        subprocess.call([self.python,"-i", module])
        print 'Exiting Python shell...'
        
    def print_help(self, line):
        if line.lower()=='help':
            print HELP
        else:
            l = line.split(' ')
            cmd, rest = l[0], ' '.join(l[1:])
            if cmd.lower() != 'help':
                return
            if rest=='m':
                print 'm <msg>: Post status message <msg>'
            elif rest=='im':
                print 'm <user> <msg>: Post direct message <msg> to user <user>'
            elif rest=='ut':
                print 'ut [<user>]: Get current user timeline without arguments\n\
                  and given user timeline with arguments'
            elif rest=='pt':
                print 'pt: Get twitter public timeline'
            elif rest=='ft':
                print "ft: Get all friends' timelines"
            elif rest=='fo':
                print 'fo: Get all follower details'
            elif rest=='f':
                print "f: Get all friends' details"
            elif rest=='dm':
                print 'dm: Get all direct messages'
            elif rest=='r':
                print 'r: Get all replies to direct messages'
            elif rest=='u':
                print 'u <user>: Get a given user details'
            elif rest=='l':
                print 'l <user> <passwd>: Set current user credentials'
            elif rest in ('i','inspect'):
                print 'i <obj_type>: Inspect object of given type'
            else:
                print 'No such command "%s"' % rest
                
        
if __name__ == "__main__":
    p = optparse.OptionParser()
    p.add_option('-u','--user',dest='user',default='',help='Optional Twitter username')
    p.add_option('-p','--passwd',dest='passw',default='',help='Optional Twitter password')

    options, args = p.parse_args()
    user, passwd = options.user, options.passw
    TwitterCmd(user, passwd).cmdloop()
