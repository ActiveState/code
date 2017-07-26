# winpaths.py

"""Functions for getting system/language/user dependent paths on windows.

All path names returned by the functions of this module are unicode strings.
"""

__all__ = [
  'HKCU', 'HKLM',
  'SHELL_FOLDERS',
  'USER_SHELL_FOLDERS',
  'expandvars',
  'get_appdata',
  'get_common_shellfolders',
  'get_homedir',
  'get_sharedconf',
  'get_shellfolders',
  'get_userconf',
  'get_windir'
]

__module__    = "winpaths"
__author__    = "Christopher Arndt"
__version__   = "0.1"
__revision__  = "$Rev$"
__date__      = "$Date$"
__copyright__ = "Python license"

# standard library modules
import _winreg, os

SHELL_FOLDERS = \
  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
USER_SHELL_FOLDERS = \
  r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
HKCU = _winreg.HKEY_CURRENT_USER
HKLM = _winreg.HKEY_LOCAL_MACHINE

# helper functions
def _substenv(m):
    return os.environ.get(m.group(1), m.group(0))

_env_rx = None
def expandvars(s):
    """Expand environment variables of form %var%.

    Unknown variables are left unchanged.
    """

    global _env_rx

    if '%' not in s:
        return s
    if _env_rx is None:
        import re
        _env_rx = re.compile(r'%([^|<>=^%]+)%')
    return _env_rx.sub(_substenv, s)

def _get_reg_value(key, subkey, name):
    """Return registry value specified by key, subkey, and name.

    Environment variables in values of type REG_EXPAND_SZ are expanded
    if possible.
    """

    key = _winreg.OpenKey(key, subkey)
    try:
        ret = _winreg.QueryValueEx(key, name)
    except WindowsError:
        return None
    else:
        key.Close()
        if ret[1] == _winreg.REG_EXPAND_SZ:
            return expandvars(ret[0])
        else:
            return ret[0]

def _get_reg_user_value(key, name):
    """Return a windows registry value from the CURRENT_USER branch."""

    return _get_reg_value(HKCU, key, name)

def _get_reg_machine_value(key, name):
    """Return a windows registry value from the LOCAL_MACHINE branch."""

    return _get_reg_value(HKLM, key, name)

# public functions
def get_appdata():
    """Return path of directory where apps should store user specific data."""

    return _get_reg_user_value(SHELL_FOLDERS, 'AppData')

def get_common_shellfolders():
    """Return mapping of shell folder names (all users) to paths."""

    return get_shellfolders(branch=HKLM)

def get_homedir():
    """Return path to user home directory, i.e. 'My Files'."""

    return _get_reg_user_value(SHELL_FOLDERS, 'Personal')

def get_sharedconf(prog, *args):
    """Return path to shared configuration data for 'prog' from 'vendor'.

    Additional arguments are appended via os.path.join().

    See also: get_user_conf()
    """

    return os.path.join(
      _get_reg_machine_value(SHELL_FOLDERS, 'Common AppData'),
      vendor, prog, *args
    )

def get_shellfolders(branch=HKCU, key=SHELL_FOLDERS):
    """Return mapping of shell folder names (current user) to paths."""

    key = _winreg.OpenKey(branch, key)
    folders = {}
    i = 0
    while True:
        try:
            ret = _winreg.EnumValue(key, i)
            if ret[2] == _winreg.REG_EXPAND_SZ:
                folders[ret[0]] = expandvars(ret[1])
            else:
                folders[ret[0]] = ret[1]
        except WindowsError:
            break
        i +=1
    key.Close()
    return folders

def get_userconf(vendor, prog, *args):
    """Return path to user configuration data for 'prog' from 'vendor'.

    Additional arguments are appended via os.path.join(), e.g.
    use like this:

    optionsfn = get_userconf("ACME Soft", "Exploder", "Options.xml")
    """

    return os.path.join(get_appdata(), vendor, prog, *args)

def get_windir():
    """Convenience function to get path to windows installation directory."""

    return unicode(os.environ["WINDIR"])
