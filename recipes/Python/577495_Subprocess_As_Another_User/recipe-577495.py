#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import win32con
import win32process
import win32security

from subprocess import *

__all__ = ["Popen","PIPE", "STDOUT", "call", "check_call",
    "CalledProcessError", "CREATE_NEW_CONSOLE", "LoginSTARTUPINFO",
    "STARTUPINFO"]

class LoginSTARTUPINFO(object):
    """
    Special STARTUPINFO instance that carries login credentials. When a
    LoginSTARTUPINFO instance is used with Popen, the process will be executed
    with the credentials used to instantiate the class.

    If an existing vanilla STARTUPINFO instance needs to be converted, it
    can be supplied as the last parameter when instantiating LoginSTARTUPINFO.

    The LoginSTARTUPINFO cannot be used with the regular subprocess module.

    >>> import subprocesswin32 as subprocess
    >>> sysuser = LoginSTARTUPINFO("username", "pswd123", "machine")
    >>> stdout, stderr = subprocess.Popen("cmd.exe", stdout=subprocess.PIPE,
    ...     startupinfo=sysuser).communicate()
    """
    def __init__(self, username, domain, password, startupinfo=None):
        m_startupinfo = win32process.STARTUPINFO()

        # Creates an actual win32 STARTUPINFO class using the attributes
        # of whatever STARTUPINFO-like object we are passed.
        for attr in dir(startupinfo):
            if not(attr.startswith("_") or attr not in dir(m_startupinfo)):
                setattr(m_startupinfo, attr, getattr(startupinfo, attr))

        # Login credentials
        self.credentials = (username, domain, password)
        # Proper win32 STARTUPINFO representation for CreateProcess
        self.win32startupinfo = m_startupinfo

def CreateProcess(*args):
    startupinfo = args[-1]

    # If we are passed a LoginSTARTUPINFO, that means we need to use
    # CreateProcessAsUser instead of the CreateProcess in subprocess
    if isinstance(startupinfo, LoginSTARTUPINFO):
        # Gets the actual win32 STARTUPINFO object from LoginSTARTUPINFO
        win32startupinfo = startupinfo.win32startupinfo

        mkprocargs = args[:-1] + (win32startupinfo,)

        login, domain, password = startupinfo.credentials

        # Get a user handle from the credentials
        userhandle = win32security.LogonUser(login, domain, password,
            win32con.LOGON32_LOGON_INTERACTIVE,
            win32con.LOGON32_PROVIDER_DEFAULT)

        try:
            # Return the pipes from CreateProcessAsUser
            return win32process.CreateProcessAsUser(userhandle, *mkprocargs)
        finally:
            # Close the userhandle before throwing whatever error arises
            userhandle.Close()

    return win32process.CreateProcess(*args)

# Overrides the CreateProcess module of subprocess with ours. CreateProcess
# will automatically act like the original CreateProcess when it is not passed
# a LoginSTARTUPINFO object.
STARTUPINFO = subprocess.STARTUPINFO = win32process.STARTUPINFO
subprocess._subprocess.CreateProcess = CreateProcess
