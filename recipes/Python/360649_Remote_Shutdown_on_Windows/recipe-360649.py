#!/usr/bin/env python
# win32shutdown.py

import win32api
import win32con
import win32netcon
import win32security
import win32wnet


def shutdown(host=None, user=None, passwrd=None, msg=None, timeout=0, force=1,
             reboot=0):
    """ Shuts down a remote computer, requires NT-BASED OS. """
    
    # Create an initial connection if a username & password is given.
    connected = 0
    if user and passwrd:
        try:
            win32wnet.WNetAddConnection2(win32netcon.RESOURCETYPE_ANY, None,
                                         ''.join([r'\\', host]), None, user,
                                         passwrd)
        # Don't fail on error, it might just work without the connection.
        except:
            pass
        else:
            connected = 1
    # We need the remote shutdown or shutdown privileges.
    p1 = win32security.LookupPrivilegeValue(host, win32con.SE_SHUTDOWN_NAME)
    p2 = win32security.LookupPrivilegeValue(host,
                                            win32con.SE_REMOTE_SHUTDOWN_NAME)
    newstate = [(p1, win32con.SE_PRIVILEGE_ENABLED),
                (p2, win32con.SE_PRIVILEGE_ENABLED)]
    # Grab the token and adjust its privileges.
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                           win32con.TOKEN_ALL_ACCESS)
    win32security.AdjustTokenPrivileges(htoken, False, newstate)
    win32api.InitiateSystemShutdown(host, msg, timeout, force, reboot)
    # Release the previous connection.
    if connected:
        win32wnet.WNetCancelConnection2(''.join([r'\\', host]), 0, 0)


if __name__ == '__main__':
    # Immediate shutdown.
    shutdown('salespc1', 'admin', 'secret', None, 0)
    # Delayed shutdown 30 secs.
    shutdown('salespc1', 'admin', 'secret', 'Maintenance Shutdown', 30)
    # Reboot
    shutdown('salespc1', 'admin', 'secret', None, 0, reboot=1)
    # Shutdown the local pc
    shutdown(None, 'admin', 'secret', None, 0)
