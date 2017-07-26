from win32com.client import (
    GetObject,
    Dispatch,
    )
from pythoncom import (
    com_error,
    )

# --------- #

Connection = Dispatch("ADODB.Connection")

Connection.Open("Provider=ADSDSOObject")

# --------- #

class Bunch(dict):
    def __init__(self,**kw):
        dict.__init__(self,kw)
        self.__dict__ = self
        
def LDAP_select_all_iterator(LDAP_path_str):

    R = Connection.Execute(
        "SELECT * From '%s'" % LDAP_path_str)[0]

    while not R.EOF:

        d = Bunch()
        for f in R.Fields:
            d[f.Name] = f.Value
        yield d

        R.MoveNext()

class LDAP_ObjectWrapper(object):

    def __init__(self, WINCOM_LDAP_Object):
        self._o = WINCOM_LDAP_Object

    @classmethod
    def from_LDAP_path(cls, LDAP_path_str):
        return cls(GetObject(LDAP_path_str))

    def __getattr__(self, name):
        try:
            return getattr(self._o, name)
        except (AttributeError, com_error):
            pass
        try:
            return self._o.Get(name)
        except com_error:
            raise AttributeError
        raise AssertionError

    def GetInfo(self):
        self._o.GetInfo()

# --------- #

defaultNamingContext = (
    LDAP_ObjectWrapper.from_LDAP_path(
        'LDAP://rootDSE').defaultNamingContext)

# --------- #
                     
results = {}

def _latin_lower(u):
    return u.encode('latin-1').lower()

for r in LDAP_select_all_iterator(
    'LDAP://CN=Users,%s' % (defaultNamingContext,)):
    
    UserObject = LDAP_ObjectWrapper.from_LDAP_path(r.ADsPath)
    UserObject.GetInfo()

    if getattr(UserObject, 'AccountDisabled', False):
        continue

    try:
        proxyAddresses = list(UserObject.proxyAddresses)
    except (AttributeError, TypeError):
        proxyAddresses = []

    if not proxyAddresses:
        continue

    email_addresses = []
    for s in proxyAddresses:
        if s.startswith('SMTP:'):
            email_addresses.append(
                ('MAIN', _latin_lower(s[5:])))
        elif s.startswith('smtp:'):
            email_addresses.append(
                ('alias', _latin_lower(s[5:])))

    if not email_addresses:
        continue
    
    email_addresses.sort()
        
    misc_info = []
    for n in ['displayName', 'name', 'description']:
        try:
            v = getattr(UserObject, n)
        except AttributeError:
            pass
        else:
            if v:
                misc_info.append(
                    repr(v.encode('latin-1')))
    assert misc_info
    description_str = ' '.join(misc_info)

    key = email_addresses[0][1]

    assert key not in results    

    results[key] = (description_str, email_addresses)

for (i, key) in enumerate(sorted(results.keys())):
    description_str, email_addresses = results[key]
    print i, description_str
    for t in email_addresses:
        print '    %-5s %s' % t
