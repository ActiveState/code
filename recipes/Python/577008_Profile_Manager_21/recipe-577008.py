## -------------------------------------------------------------------------- ##
##  Profile Manager.py                                                        ##
## -------------------------------------------------------------------------- ##

import os
import cmd
import sys
import spice
import random
import cStringIO

################################################################################

class Interface(cmd.Cmd):

    def preloop(self):
        'Setup the command prompt.'
        self.prompt = '>>> '
        self.intro = 'CS Profile Manager v2.1'
        self.intro += '\n' + self.ruler * len(self.intro)
        self.use_rawinput = False
        self.cmdqueue.extend(sys.argv[1:])
        try:
            self.control = Profile_Manager('Profile.dat', 'save',
                                           'Doukutsu.exe', 1478656, 260997856)
            self.error = False
        except Exception, reason:
            self.reason = reason
            self.error = True

    def precmd(self, line):
        'Look for Profile_Manager error.'
        if self.error:
            return 'quit'
        return line

    def postloop(self):
        'Provide proper shutdown messages.'
        if self.error:
            self.stdout.write(self.reason.message)
        else:
            self.stdout.write('Goodbye.')

    def do_shell(self, arg):
        'shell <arg>\nPass argument to the command prompt.'
        os.system(arg)

    def do_save(self, arg):
        'save <arg>\nSave profile by name or alias.'
        try:
            self.control.save(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_list(self, arg):
        'list\nList profiles with their aliases.'
        array = self.control.list()
        if array:
            for alias, name in enumerate(array):
                self.stdout.write('(%s) %s\n' % (alias + 1, name))
        else:
            self.stdout.write('NO PROFILES LOADED\n')

    def do_load(self, arg):
        'load <arg>\nLoad profile by name or alias.'
        try:
            self.control.load(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_away(self, arg):
        'away <arg>\nDelete profile by name or alias.'
        try:
            self.control.away(arg)
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_quit(self, arg):
        'quit\nExit the profile manager.'
        return True

    def do_export(self, arg):
        'export <arg>\nExport profiles to specified file.'
        try:
            self.control.export_(arg, 'Doukutsu Monogatari')
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

    def do_import(self, arg):
        'import <arg>\nImport profiles from specified file.'
        try:
            self.control.import_(arg, 'Doukutsu Monogatari')
        except Exception, reason:
            self.stdout.write(reason.message + '\n')

################################################################################

class Profile_Manager:

    STRING = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    def __init__(self, filename, savepath,
                 testfile=None, testsize=None, testhash=None):
        'Initialize the Profile Manager object.'
        if testfile is not None:
            self.test(testfile, testsize, testhash)
        self.filename = filename
        self.savepath = savepath
        self.autoload()

    def test(self, testfile, testsize, testhash):
        'Perform tests instructed by the caller.'
        assert os.path.exists(testfile), '%r does not exist.' % testfile
        assert os.path.isfile(testfile), '%r is not a file.' % testfile
        if testsize is not None:
            assert os.path.getsize(testfile) == testsize, \
                   '%r has an invalid size.' % testfile
        if testhash is not None:
            assert hash(file(testfile, 'rb').read()) == testhash, \
                   '%r has an invalid hash.' % testfile

    def autoload(self):
        'Automatically load available profiles.'
        self.profiles = {}
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)
        else:
            for path, dirs, data in os.walk(self.savepath):
                for name in data:
                    self.autoread(os.path.join(path, name))
        self.aliases = self.profiles.keys()

    def autoread(self, pathname):
        'Read in profiles from their pathnames.'
        # Create the keys.
        random.seed(int(os.path.getctime(pathname)))
        major = spice.major()
        minor = spice.minor()
        random.seed() # Restore randomness.
        # Decode the file.
        string = cStringIO.StringIO()
        spice.decode(file(pathname, 'rb'), string, major, minor)
        string = string.getvalue()
        # Extract the data.
        namesize = ord(string[0]) + 2
        name = string[1:namesize]
        profile = string[namesize:]
        # Archive the data.
        assert profile, '%r has no profile data.' % pathname
        self.profiles[name] = [profile, pathname, major, minor]

    def save(self, arg):
        'Save profile with name and archive.'
        assert os.path.exists(self.filename), '%r NOT FOUND' % self.filename
        assert 1 <= len(arg) <= 256, 'BAD NAME LENGTH'
        arg = self.solve(arg, False)
        profile = file(self.filename, 'rb').read()
        if arg in self.profiles:
            # Update profile and get save info.
            self.profiles[arg][0] = profile
            pathname, major, minor = self.profiles[arg][1:]
            destination = open(pathname, 'wb')
        else:
            destination, major, minor = self.save_new(arg, profile)
        self.save_act(arg, profile, destination, major, minor)

    def save_new(self, arg, profile):
        'Prepare to write a new profile.'
        # Create a pathname.
        name = ''.join(random.sample(self.STRING, len(self.STRING)))
        pathname = os.path.join(self.savepath, name)
        while os.path.exists(pathname):
            name = ''.join(random.sample(self.STRING, len(self.STRING)))
            pathname = os.path.join(self.savepath, name)
        # Create destination and keys.
        destination = open(pathname, 'wb')
        random.seed(int(os.path.getctime(pathname)))
        major = spice.major()
        minor = spice.minor()
        random.seed() # Restore randomness.
        # Create a new profile entry.
        self.profiles[arg] = [profile, pathname, major, minor]
        self.aliases.append(arg)
        return destination, major, minor

    def save_act(self, arg, profile, destination, major, minor):
        'Encrypt and save profile to disk.'
        source = cStringIO.StringIO(chr(len(arg) - 1) + arg + profile)
        spice.encode(source, destination, major, minor)
        destination.close()        

    def list(self):
        'Return an array of loaded profiles.'
        return tuple(self.aliases)

    def load(self, arg):
        'Load an archived profile for use.'
        arg = self.solve(arg)
        profile = self.profiles[arg][0]
        file(self.filename, 'wb').write(profile)

    def away(self, arg):
        'Detele the specified profile.'
        arg = self.solve(arg)
        os.remove(self.profiles[arg][1])
        del self.profiles[arg]
        self.aliases.remove(arg)

    def solve(self, arg, require=True):
        'Solve profile alias if given.'
        if arg not in self.profiles:
            try:
                index = int(arg) - 1
            except:
                if require:
                    raise Exception('%r NOT FOUND' % arg)
                return arg
            assert self.aliases, 'NO PROFILES LOADED'
            try:
                assert index > -1
                return self.aliases[index]
            except:
                raise Exception('INDEX OUT OF BOUNDS')
        return arg

    def export_(self, arg, key):
        'Encode all profiles and export them.'
        try:
            destination = open(arg, 'wb')
        except:
            raise Exception('%r CANNOT BE CREATED' % arg)
        random.seed(key)
        major = spice.major()
        minor = spice.minor()
        random.seed() # Restore randomness.
        for name in self.aliases:
            profile = self.profiles[name][0]
            assert len(profile) <= 16777216, '%r IS TOO LARGE' % name
            len_name = chr(len(name) - 1)
            len_profile = self.str_(len(profile) - 1)
            source = cStringIO.StringIO(len_name + len_profile + name + profile)
            spice.encode(source, destination, major, minor)
        destination.close()

    def str_(self, number):
        'Convert number into a string.'
        string = ''
        for byte in range(3):
            string = chr(number & 0xFF) + string
            number >>= 8
        return string

    def import_(self, arg, key):
        'Import all profiles and decode them.'
        # Decode the data being imported.
        try:
            source = open(arg, 'rb')
        except:
            raise Exception('%r CANNOT BE OPENED' % arg)
        random.seed(key)
        major = spice.major()
        minor = spice.minor()
        random.seed() # Restore randomness.
        destination = cStringIO.StringIO()
        spice.decode(source, destination, major, minor)
        source.close()
        destination.seek(0)
        # Import the decoded profiles.
        len_name = destination.read(1)
        while len_name:
            len_profile = destination.read(3)
            assert len(len_profile) == 3, '%r IS CORRUPT' % arg
            len_name = ord(len_name) + 1
            name = destination.read(len_name)
            assert len(name) == len_name, '%r IS CORRUPT' % arg
            len_profile = self.int_(len_profile) + 1
            profile = destination.read(len_profile)
            assert len(profile) == len_profile, '%r IS CORRUPT' % arg
            # Check for duplicate names.
            if name in self.aliases:
                name = name[:250]
                code = ''.join(random.sample(self.STRING, 3))
                temp = '%s [%s]' % (name, code)
                while temp in self.aliases:
                    code = ''.join(random.sample(self.STRING, 3))
                    temp = '%s [%s]' % (name, code)
                name = temp
            # Save the new profile to disk.
            self.save_act(name, profile, *self.save_new(name, profile))
            len_name = destination.read(1)

    def int_(self, string):
        'Convert string into a number.'
        number = 0
        for character in string:
            number <<= 8
            number += ord(character)
        return number

################################################################################

if __name__ == '__main__':
    Interface().cmdloop()

## -------------------------------------------------------------------------- ##
##  spice.py                                                                  ##
## -------------------------------------------------------------------------- ##

'''Module that implements SPICE.

This module provides access to a standardized implementation
of SPICE (Stephen's Power-Inspired, Computerized Encryption).'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'March 19, 2008'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
T. Parker, for testing code that led to this module.
A. Baddeley, for contributing to the random module.
R. Hettinger, for adding support for two core generators.'''

################################################################################

import random as _random
import sys as _sys

################################################################################

def major():
    'Create a new Major Key.'
    return ''.join(map(chr, _random.sample(xrange(256), 256)))

def minor():
    'Create a new Minor Key.'
    sample = _random.sample(range(4) * 64, 256)
    return ''.join(map(chr, ((sample[index * 4] << 6) + (sample[index * 4 + 1] << 4) + (sample[index * 4 + 2] << 2) + sample[index * 4 + 3] for index in xrange(64))))

def encode(source, destination, major_key, minor_key):
    'Encode from source to destination via Major and Minor Keys.'
    _check_major(major_key)
    _check_minor(minor_key)
    map_1 = map(ord, major_key)
    map_2 = _setup_minor(minor_key)
    character = source.read(1)
    while character:
        byte = map_1[ord(character)]
        for shift in xrange(6, -2, -2):
            destination.write(map_2[(byte >> shift) & 3][_random.randrange(64)])
        character = source.read(1)
    destination.flush()

def decode(source, destination, major_key, minor_key):
    'Decode from source to destination via Major and Minor Keys.'
    _check_major(major_key)
    _check_minor(minor_key)
    map_1 = [(byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)]
    map_2 = _setup_major(major_key)
    double_word = source.read(4)
    while double_word:
        destination.write(map_2[(map_1[ord(double_word[0])] << 6) + (map_1[ord(double_word[1])] << 4) + (map_1[ord(double_word[2])] << 2) + map_1[ord(double_word[3])]])
        double_word = source.read(4)
    destination.flush()

################################################################################

def _check_major(major_key):
    'Private module function.'
    assert isinstance(major_key, str) and len(major_key) == 256
    for character in map(chr, xrange(256)):
        assert character in major_key

def _check_minor(minor_key):
    'Private module function.'
    assert isinstance(minor_key, str) and len(minor_key) == 64
    indexs = [(byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)]
    for index in xrange(4):
        assert indexs.count(index) == 64

def _setup_minor(minor_key):
    'Private module function.'
    map_2 = [[], [], [], []]
    for byte, index in enumerate((byte >> shift) & 3 for byte in map(ord, minor_key) for shift in xrange(6, -2, -2)):
        map_2[index].append(chr(byte))
    return map_2

def _setup_major(major_key):
    'Private module function.'
    map_2 = [None] * 256
    for byte, index in enumerate(map(ord, major_key)):
        map_2[index] = chr(byte)
    return map_2

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
