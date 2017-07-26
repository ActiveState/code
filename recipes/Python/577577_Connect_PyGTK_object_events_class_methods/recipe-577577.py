#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Connecting PyGTK object events to class methods automatically.

Helps you not to repeat yourself (DRY) with PyGTK. Example:

from pygtkconnect import *
class MyClass:
    (...)
    @gtk_event 
    def my_button_clicked(self, widget, data=None):
        (...)

    def __init__(self):
        (...)
        gtk_insert(self, 'my_button', gtk.Button('click me'))
        # also does self.my_button = ...
        (...)
        gtk_connect_events(self)
        # calls self.my_button.connect('clicked', self.my_button_clicked)
        # and similar for all decorated methods in one line of code :)

If you call gtk_connect_events(self, False), you can even skip the
@gtk_event decorators, but then you have to be careful with method names!
'''

__author__ = 'Pavel Krc'
__email__ = 'pk-alt@seznam.cz'
__date__ ='2011-02-17'
__all__ = ['gtk_event', 'gtk_insert', 'gtk_connect_events', 'PygtkconnectException']


import re

class PygtkconnectException(Exception):
    pass

def gtk_event(method):
    '''A decorator that makes a method connectible to an event

    The method name must be exactly [_[_]]membername_eventname.
    '''
    method._pygtkconnect_method_is_event = True
    return method

def gtk_insert(user_object, member_name, gtk_object, insert_as_member=True):
    '''Enables PyGTK event binding for a PyGTK object

    You must make sure that the member names are not ambiguous, i.e. if you
    remove leading underscores from member names, then a member name with added
    underscore at the end isn't a prefix of some other member name. "member"
    and "member1" are OK, "__member" and "member_two" are not.
    
    If insert_as_member is True, the gtk object is also inserted as a member to
    user_object (using member_name).
    '''
    if not hasattr(user_object, '__pygtkconnect_members'):
        user_object.__pygtkconnect_members = {member_name: gtk_object}
    else:
        user_object.__pygtkconnect_members[member_name] = gtk_object

    if insert_as_member:
        setattr(user_object, member_name, gtk_object)

def gtk_connect_events(user_object, require_decorators=True):
    '''Connects decorated event methods as event handlers to selected members
    
    If require_decorators is False, the methods used as events are determined
    purely by name prefix (be careful!).
    '''
    members = user_object.__pygtkconnect_members
    if require_decorators:
        funcs = [name for name, obj
                in user_object.__class__.__dict__.iteritems()
                if hasattr(obj, '_pygtkconnect_method_is_event')]
    else:
        funcs = [name for name, obj
                in user_object.__class__.__dict__.iteritems()
                if callable(obj)]

    # create a regex with member names for separating member name and event
    names_reg = re.compile('^(_{0,2})(%s)_(.*)$' %
            '|'.join(members.iterkeys()))

    # connect it all
    for funcname in funcs:
        m = names_reg.match(funcname)
        if not m:
            if require_decorators:
                raise PygtkconnectException('Invalid method name or no matched '
                    'member object!')
            else:
                continue
        leading_uscores, member_name, event_name = m.groups()
        members[member_name].connect(event_name, getattr(user_object, funcname))
