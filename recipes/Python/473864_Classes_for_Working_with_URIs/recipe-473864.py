from urlparse import urlparse

class Authority(dict):
    '''
    >>> a = Authority('username:asecret@host.com:443')
    >>> a.user
    'username'
    >>> a.password
    'asecret'
    >>> a.host
    'host.com'
    >>> a.port
    443

    # You can also access these like a dict, if you prefer
    >>> a['user']
    'username'
    >>> a['password']
    'asecret'

    # What about an authority section  with no password?
    >>> a = Authority('username@host.com:443')
    >>> a.user
    'username'
    >>> a.password # no return value

    # What about an empty password?
    >>> a = Authority('username:@host.com:443')
    >>> a.user
    'username'
    >>> a.password
    ''

    # A simpler authority:
    >>> a = Authority('host.com:8080')
    >>> a.host
    'host.com'
    >>> a.port
    8080
    '''
    def __init__(self, auth):
        self.auth = auth
        auths = auth.split('@')
        if len(auths) == 2:
            userpass = auths.pop(0)
            userpass = userpass.split(':')
            self.user = userpass.pop(0)
            try:
                self.password = userpass.pop(0)
            except:
                self.password = None
        else:
            self.user = self.password = None
        hostport = auths[0].split(':')
        self.host = hostport.pop(0)
        try:
            self.port = int(hostport.pop(0))
        except:
            self.port = None
        attrs = [ (attr, getattr(self, attr)) 
            for attr in ('user', 'password', 'host', 'port') ]
        self.update(dict(attrs))
            

class UriQuery(dict):
    '''
    >>> query_string = 'num=100&q=twisted+python&btnG=Search'
    >>> query = UriQuery(query_string)
    >>> query['q']
    'twisted+python'
    >>> k = query.keys()
    >>> k.sort();k
    ['btnG', 'num', 'q']
    >>> v = query.values()
    >>> v.sort();v
    ['100', 'Search', 'twisted+python']
    '''
    def __init__(self, query):
        self.query = query
        if query:
            query_dict = dict([x.split('=') for x in query.split('&') ])
            self.update(query_dict)
            for key, val in query_dict.items():
                setattr(self, key, val)

class Uri(object):
    '''
    >>> url = 'ftp://username:asecret@ftp.funet.fi/pub/NeXT'
    >>> uri = Uri(url)
    >>> (uri.scheme, uri.user, uri.password, uri.host, uri.port, uri.path)
    ('ftp', 'username', 'asecret', 'ftp.funet.fi', None, '/pub/NeXT')

    >>> url = 'http://www.google.com/search?num=100&q=twisted+python&btnG=Search'
    >>> uri = Uri(url)
    >>> (uri.scheme, uri.path)
    ('http', '/search')
    >>> uri.query.q
    'twisted+python'
    '''
    def __init__(self, uri):
        (self.scheme, netloc, path, self.params, query, 
            self.fragment) = urlparse(uri)

        self.authority = Authority(netloc)
        self.path = path or '/'
        self.query = UriQuery(query)
        # for convenience:
        self.user = self.authority.user
        self.password = self.authority.password
        self.host = self.authority.host
        self.port = self.authority.port

def _test():
    import doctest, uri
    doctest.testmod(uri)

if __name__ == '__main__':
    _test()
