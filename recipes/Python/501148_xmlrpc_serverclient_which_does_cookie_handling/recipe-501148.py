#### server.py 
import uuid
import base64
import socket
import shelve
import Cookie
from SimpleXMLRPCServer import *  

class UserManagement:
    def __init__(self):
        self.d = shelve.open('machines.shv')

        # register a list of valid machine names/email id's 
        validconfig = {'email@address.com':'vaikings'}
        for k,v in validconfig.items():
            self.generateUuid(k,v)

    def generateUuid(self, email_id, machine_name):
        """ return a uuid which uniquely identifies machinename and email id """
        uuidstr = None

        if machine_name not in self.d:
            myNamespace = uuid.uuid3(uuid.NAMESPACE_URL, machine_name)
            uuidstr = str(uuid.uuid3(myNamespace, email_id)) 

            self.d[machine_name] = (machine_name, uuidstr, email_id)
            self.d[uuidstr] = (machine_name, uuidstr ,email_id)
        else:
            (machine_name, uuidstr, email_id) = self.d[machine_name]

        return uuidstr

    def checkMe(self, id):
        if id in self.d:
            return self.d[id]
        return (None,None,None)

    def __del__(self):
        self.d.close()

def authenticate(id):
    sk = UserManagement()
    return sk.checkMe(id)

class MySimpleXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    def setCookie(self, key=None ,value=None):
        if key :
            c1 = Cookie.SimpleCookie()
            c1[key] = value
            cinfo = self.getDefaultCinfo() 
            for attr,val in cinfo.items():
                c1[key][attr] = val
                            
            if c1 not in self.cookies:
                self.cookies.append(c1)

    def getDefaultCinfo(self):
        cinfo = {}

        cinfo['expires'] = 30*24*60*60
        cinfo['path'] = '/RPC2/'
        cinfo['comment'] = 'comment!'
        cinfo['domain'] = '.localhost.local'
        cinfo['max-age'] = 30*24*60*60
        cinfo['secure'] = ''
        cinfo['version']= 1
        
        return cinfo
                            
    def do_POST(self):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as XML-RPC calls,
        which are forwarded to the server's _dispatch method for handling.
        """
        #Note: this method is the same as in SimpleXMLRPCRequestHandler, 
        #just hacked to handle cookies 

        # Check that the path is legal
        if not self.is_rpc_path_valid():
            self.report_404()
            return

        try:
            # Get arguments by reading body of request.
            # We read this in chunks to avoid straining
            # socket.read(); around the 10 or 15Mb mark, some platforms
            # begin to have problems (bug #792570).
            max_chunk_size = 10*1024*1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                L.append(self.rfile.read(chunk_size))
                size_remaining -= len(L[-1])
            data = ''.join(L)

            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))

            # HACK :start -> sends cookies here 
            if self.cookies:
                for cookie in self.cookies:
                    self.send_header('Set-Cookie',cookie.output(header=''))
            # HACK :end
            
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

    def authenticate_client(self):
        validuser = False

        if self.headers.has_key('Authorization'):
            # handle Basic authentication
            (enctype, encstr) =  self.headers.get('Authorization').split()
            (emailid, machine_name) = base64.standard_b64decode(encstr).split(':')
            (auth_machine, auth_uuidstr, auth_email) = authenticate(machine_name)

            if emailid == auth_email:
                print "Authenticated"
                # set authentication cookies on client machines
                validuser = True
                if auth_uuidstr:
                    self.setCookie('UUID',auth_uuidstr)
                    
        elif self.headers.has_key('UUID'):
            # handle cookie based authentication
            id =  self.headers.get('UUID')
            (auth_machine, auth_uuidstr, auth_email) = authenticate(id)

            if auth_uuidstr :
                print "Authenticated"
                validuser = True
        else:
            print 'Authentication failed'

        return validuser

    def _dispatch(self, method, params):    
        self.cookies = []
        
        validuser = self.authenticate_client() 
        # handle request        
        if method == 'hello_world':                
            (input1, input2) = params    
            retstr = XMLRPC_register().hello_world(input1, input2, validuser)
            return retstr
        else:
            return 'Invalid Method [%s]'%method

# functions available as web services
class XMLRPC_register:
    def hello_world(self, t1, t2, validuser):
        if validuser:
            return t1+'-'+t2
        else:
            return "please register ur machine"

if __name__ == '__main__':
    try:
        se = SimpleXMLRPCServer(("localhost",8088), MySimpleXMLRPCRequestHandler, True, True)
        se.register_introspection_functions()
        se.serve_forever()
    except KeyboardInterrupt:
        print "Bye"
    
#--------------------- new file starts here-----------
### client.py 
import os
import base64
import xmlrpclib
import urllib2
import cookielib

class CookieAuthXMLRPCTransport(xmlrpclib.Transport):
    """ xmlrpclib.Transport that sends basic HTTP Authentication"""

    user_agent = '*py*'
    credentials = ()
    cookiefile = 'cookies.lwp'
        
    def send_basic_auth(self, connection):
        """Include HTTP Basic Authentication data in a header"""
        
        auth = base64.encodestring("%s:%s"%self.credentials).strip()
        auth = 'Basic %s' %(auth,)
        connection.putheader('Authorization',auth)

    def send_cookie_auth(self, connection):
        """Include Cookie Authentication data in a header"""
        
        cj = cookielib.LWPCookieJar()
        cj.load(self.cookiefile)

        for cookie in cj:
            if cookie.name == 'UUID':
                uuidstr = cookie.value
            connection.putheader(cookie.name, cookie.value)

    ## override the send_host hook to also send authentication info
    def send_host(self, connection, host):
        xmlrpclib.Transport.send_host(self, connection, host)
        if os.path.exists(self.cookiefile):
            self.send_cookie_auth(connection)
        elif self.credentials != ():
            self.send_basic_auth(connection)
                    
    def request(self, host, handler, request_body, verbose=0):
        # dummy request class for extracting cookies 
        class CookieRequest(urllib2.Request):
            pass
            
        # dummy response class for extracting cookies 
        class CookieResponse:
            def __init__(self, headers):
                self.headers = headers
            def info(self):
                return self.headers 

        crequest = CookieRequest('http://'+host+'/')
            
        # issue XML-RPC request
        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        self.send_request(h, handler, request_body)
        self.send_host(h, host)
        self.send_user_agent(h)
        
        # creating a cookie jar for my cookies
        cj = cookielib.LWPCookieJar()
                        
        self.send_content(h, request_body)
            
        errcode, errmsg, headers = h.getreply()

        cresponse = CookieResponse(headers)
        cj.extract_cookies(cresponse, crequest)

        if len(cj) >0 and self.cookiefile != None:
            cj.save(self.cookiefile)
                
        if errcode != 200:
            raise ProtocolError(
                host + handler,
                errcode, errmsg,
                headers
                )

        self.verbose = verbose

        try:
            sock = h._conn.sock
        except AttributeError:
            sock = None
                
        return self._parse_response(h.getfile(), sock)

def getXmlrpcClient(server_uri, auth = ()):
    """ this will return an xmlrpc client which supports
    basic authentication/authentication through cookies 
    """

    trans = CookieAuthXMLRPCTransport()
    if auth!= ():
        trans.credentials = auth
    client = xmlrpclib.Server(server_uri, transport=trans, verbose=False)
    
    return client

if __name__ == "__main__":
    email = 'email@address.com'
    machine_name = 'vaikings'
    
    client = getXmlrpcClient('http://localhost:8088', (email,machine_name))
#    client = getXmlrpcClient('http://localhost:8088')
    inputstr1 = "hello"
    inputstr2 = "world"

    try:
        retstr = client.hello_world(inputstr1, inputstr2)
        print retstr

        print client.hey('hey')
    except Exception, e:
        print e
