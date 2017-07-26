from win32com.client import (
    GetObject,
    Dispatch,
    )

from pythoncom import (
    com_error,
    )

import datetime

import re

from textwrap import fill

# --------- #

__test__ = {}

# --------- #

# 12/30/1899, the zero-Date for ADO = 693594
_ADO_zeroHour = datetime.date(1899, 12, 30).toordinal()

_time_zero = datetime.time(0, 0, 0)

def ADO_PyTime_To_Datetime(v):
    
    v_date, v_time = divmod(float(v), 1)
    datetime_date = datetime.date.fromordinal(
        int(round(v_date + _ADO_zeroHour)))
    v_time = int(round(86400 * v_time))
    v_hour, v_min = divmod(v_time, 3600)
    v_min, v_sec = divmod(v_min, 60)
    datetime_time = datetime.time(
        int(v_hour), int(v_min), int(v_sec))
    return (datetime_date, datetime_time)

# --------- #

class SentinalSingleton(object):
    def __str__(self):
        return self.__class__.__name__
    __repr__ = __str__

class UntranslatableCOM(SentinalSingleton):
    pass 

UntranslatableCOM = UntranslatableCOM()

class UnrecognizedCOM(SentinalSingleton):
    pass

UnrecognizedCOM = UnrecognizedCOM()

re_read_write_buffer = re.compile(
    r'^\<read-write buffer '
     'ptr 0x([0-9A-F]+)\, '
     'size ([0-9A-F]+) '
     'at 0x([0-9A-F]+)\>$')

__test__['re_read_write_buffer'] = r'''

    >>> bool(re_read_write_buffer.match(
    ...     '<read-write buffer ptr 0x00A4DF40, size 28 at 0x00A4DF20>'))
    True
    
'''

def _process_COM_value(V):
    """
    
    >>> _process_COM_value(3)
    3
    >>> _process_COM_value((3, 3, 3))
    [3, 3, 3]
    >>> _process_COM_value((UntranslatableCOM, UntranslatableCOM))
    UntranslatableCOM
    >>> _process_COM_value((UntranslatableCOM, 3))
    [UntranslatableCOM, 3]
    >>> _process_COM_value((UntranslatableCOM, UnrecognizedCOM))
    [UntranslatableCOM, UnrecognizedCOM]
    
    """
    
    if V in [UntranslatableCOM, UnrecognizedCOM, None]:
        
        return V
    
    elif isinstance(
        V,
        (
            str,
            float,
            int,
            long,
            datetime.date,
            datetime.time,
            datetime.datetime,
            )):
        
        return V
        
    elif isinstance(V, unicode):
        
        try:
            return V.encode('latin-1')
        except UnicodeEncodeError:
            return V
        
    elif isinstance(V, (tuple, list)):
        L = map(_process_COM_value, V)
        if L == ([UntranslatableCOM] * len(L)):
            return UntranslatableCOM
        else:
            return L
        
    elif type(V).__name__ == 'time':
        
        d, t = ADO_PyTime_To_Datetime(V)
        if t == _time_zero:
            return d
        else:
            return datetime.datetime.combine(d, t)
        
    else:
        
        R = repr(V)
    
        if R == '<COMObject <unknown>>':
            
            return UntranslatableCOM
        
        elif re_read_write_buffer.match(R):
            
            return UntranslatableCOM
        
        else:
            
            return UnrecognizedCOM
            
            #for S in ['V', 'type(V)', 'str(V)', 'repr(V)', 'type(V).__name__']:
            #    print '%s: %r' % (S, eval(S))
            #
            #raise ValueError, V

# --------- #

class LDAP_COM_Wrapper(object):

    def __init__(self, LDAP_COM_Object):
        
        self.__dict__[None] = LDAP_COM_Object

    def __getattr__(self, name):
        
        LDAP_COM_Object = self.__dict__[None]
        
        try:
            V = LDAP_COM_Object.Get(name)
        except com_error:
            pass
        else:
            return _process_COM_value(V)
        
        try:
            V = getattr(LDAP_COM_Object, name)
        except (AttributeError, com_error):
            pass
        else:
            return _process_COM_value(V)
        
        raise AttributeError
    
    def __getitem__(self, name):
        
        _getattr = self.__getattr__
        
        try:
            return _getattr(name)
        except AttributeError:
            raise KeyError

def LDAP_COM_to_dict(X):
    
    d = {}
    for i in range(X.PropertyCount):
        P = X.Item(i)
        Name = P.Name
        d[Name] = _process_COM_value(X.Get(Name))
    return d
        
def LDAP_select_all_iterator(Connection, LDAP_query_string):

    R = Connection.Execute(LDAP_query_string)[0]

    while not R.EOF:
        
        d = {}
        for f in R.Fields:
            d[f.Name] = _process_COM_value(f.Value)
        yield d
    
        R.MoveNext()
        
def LDAP_select_then_ADsPath_iterator(Connection, LDAP_query_string):
    
    for r in LDAP_select_all_iterator(Connection, LDAP_query_string):
    
        X = GetObject(r['ADsPath'])
        X.GetInfo()
        
        yield LDAP_COM_to_dict(X)
        
# --------- #

def _sort_helper(d):
    s = d.get('name', '<<<MISSING>>>')
    try:
        s = str(s)
    except UnicodeEncodeError:
        s = repr(s)
    return s.lower()

def _get_all_of_objectClass(
    Connection, defaultNamingContext, objectClass):
    
    LDAP_query_string = (
        "Select * "
        "from 'LDAP://%s' "
        "where objectClass = '%s'" % (
            defaultNamingContext,
            objectClass,
            ))
    
    print 'LDAP_query_string: %r' % (LDAP_query_string,)
    
    L = list(LDAP_select_then_ADsPath_iterator(
        Connection, LDAP_query_string))
    
    L.sort(key=_sort_helper)

    for d in L:
        
        print '\n'
        for k in ['name', 'description']:
            v = d.get(k, '<<<MISSING>>>')
            print fill(
                '%s: %s' % (k, v),
                width=70,
                initial_indent='',
                subsequent_indent='    ',
                )
        
        for k in sorted(d.keys()):
            try:
                k = str(k)
            except UnicodeEncodeError:
                continue
            v = d[k]
            if v is UntranslatableCOM:
                continue
            try:
                v = str(v)
            except UnicodeEncodeError:
                v = repr(v)
            print fill(
                '%s: %s' % (k, v),
                width=70,
                initial_indent='    ',
                subsequent_indent='        ',
                )
            
def main():
    
    Connection = Dispatch("ADODB.Connection")
    
    Connection.Open("Provider=ADSDSOObject")
    
    defaultNamingContext = LDAP_COM_Wrapper(
        GetObject('LDAP://rootDSE'))['defaultNamingContext']
        
    print 'defaultNamingContext: %r' % (defaultNamingContext,)
    
    for objectClass in ['computer', 'user', 'group']:
        
        print
        
        try:
            _get_all_of_objectClass(
                Connection, defaultNamingContext, objectClass)
        except com_error:
            print (
                '<<<REPORT FAILED FOR: objectClass %s>>>' % (
                    objectClass,))
        
if __name__ == '__main__':

    main()
                     
