###############
# paramset.py #
###############

class ParamSet:
    """A mutable set of parameters.
    
    data: a dictionary of the form: {Name: Value}.
    _Value_ will be a string, unless multiple parameters
    of the same _Name_ are created, in which case _Value_
    will become a list of strings.
    """
    
    data = {}
    
    def __init__(self):
        self.data = {}
    
    def add_param(self, name, value):
        name, value = str(name), str(value)
        if self.data.has_key(name):
            if type(self.data[name]) != type([]):
                # Current value is not a list.
                # Create a list for the value instead.
                self.data[name] = [self.data[name]]
            self.data[name].append(value)
        else:
            self.data[name] = value
    
    def flush(self):
        self.data = {}


#############
# uihtml.py #
#############

import re
from classloader import get_func
import paramset

class UserInterfaceHTML:
    """A base class for HTML interfaces."""
    
    requestParams = paramset.ParamSet()
    user = ''

    OK = 200
    HTTP_NOT_ACCEPTABLE = 406
    
    dispatchre = re.compile('([^/]*)\.htm$')
    dispatches = {'default': 'myapp.interface.default.view',
                  'directory': 'myapp.interface.directory.view',
                  'directoryedit': 'myapp.interface.directory.edit'}
    
    hostname = ''
    port = 80
    protocol = 'http'
    path = '/'
    script = ''
    
    def dispatch(self):
        """Process a URI and invoke the appropriate handler."""
        page = self.dispatchre.search(self.script)
        try:
            nextHandler = get_func(self.dispatches[page.group(1)])
        except KeyError:
            nextHandler = get_func(self.dispatches['default'])
        return nextHandler(self)
    
    def write_header(self, documentTitle):
        """Write a standard HTML header."""
        self.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n')
        self.write('   "http://www.w3.org/TR/xhtml1/DTD/strict.dtd">\n')
        self.write('<html xmlns="http://www.w3.org/TR/xhtml1/strict"')
        self.write(' xml:lang="en" lang="en">\n\n')
        self.write("<head>\n")
        self.write("   <title>%s</title>\n" % documentTitle)
        self.write("</head>\n")
    
    def uri_port(self):
        if self.port == 80: return ''
        return ':%s' % self.port
    
    def location(self, includeScriptName=False):
        if includeScriptName:
            return '%s://%s%s%s/%s' % (self.protocol, self.hostname,
                                       self.uri_port(), self.path,
                                       self.script)
        return '%s://%s%s%s/' % (self.protocol, self.hostname,
                                 self.uri_port(), self.path)
    

################################
# myapp.interface.directory.py #
################################

from objectkit import objectservers

def view(UI):
    """Write the requested Directory object page out to the client."""
    
    # Locate the requested Directory object.
    reqID = UI.requestParams.value('ID', '0')
    reqDir = objectservers.recall('Directory', reqID)
    
    # Write assembled page out to the client.
    UI.write_header('Directory %s' % reqID)
    UI.write("<body>You are looking at Directory record %s, %s" % \
        (reqID, reqDir.name()))
    UI.write("</body></html>")
    return UI.OK

def edit(UI):
    """Edit the requested Directory object page."""
    
    # Locate the requested Directory object.
    reqID = UI.requestParams.value('ID', '0')
    reqDir = objectservers.recall('Directory', reqID)
    reqDir.name = UI.requestParams.value('name', '')

    # Write page out to the client.
    UI.write_header('Directory %s' % reqID)
    UI.write("<body>You just edited Directory record %s, %s" % \
        (reqID, reqDir.name()))
    UI.write("</body></html>")
    return UI.OK

########### ASP ###########

############
# uiasp.py #
############

from uihtml import *
from cgi import parse_qs

class UserInterfaceASP(UserInterfaceHTML):
    """Provide an HTML interface built with Microsoft's ASP framework."""
    
    response = None
    
    def __init__(self, anApp, aRequest, aResponse):
        """Create an interface using the ASP top-level objects from a Request."""
        
        # Set response hook.
        self.response = aResponse
        
        # Set uri data from Request object.
        if aRequest.ServerVariables("HTTPS") == "ON":
            self.protocol = 'https'
        self.port = str(aRequest.ServerVariables("SERVER_PORT"))
        self.hostname = str(aRequest.ServerVariables("SERVER_NAME"))
        tName = str(aRequest.ServerVariables("SCRIPT_NAME"))
        atoms = tName.split("/")
        self.script = atoms.pop()
        self.path = "/".join(atoms)
        
        # Store logged-on username
        self.user = str(aRequest.ServerVariables("LOGON_USER"))
        
        # Retrieve the submitted CGI parameters.
        if str(aRequest.ServerVariables("REQUEST_METHOD")) == 'POST':
            self.set_params(aRequest.Form())
        else:
            self.set_params(aRequest.QueryString())
        
    def set_params(self, queryString):
        """Parse CGI params into a paramset."""
        self.requestParams.flush()
        inParams = parse_qs(str(queryString), True, False)
        for eachName, eachValue in inParams.items():
            for eachSubValue in eachValue:
                self.requestParams.add_param(eachName, eachSubValue)
    
    def write(self, textToOutput):
        self.response.Write(textToOutput)


#################################
# D:\htdocs\myapp\directory.htm #
#################################

<%@Language=Python%>
<%
from myapp.interface import uiasp

uiasp.UserInterfaceASP(Application, Request, Response).dispatch()
%>



######## mod_python #######

##################
# uimodpython.py #
##################

from uihtml import *
from mod_python import apache, util

class UserInterfaceModPython(UserInterfaceHTML):
    """Provide an HTML interface using mod_python."""

    response = None

    def __init__(self, aRequest):
        
        self.OK = apache.OK
        self.HTTP_NOT_ACCEPTABLE = apache.HTTP_NOT_ACCEPTABLE
        
        # Set response hook to equal the Request object.
        self.response = aRequest
        self.load_params(aRequest)
        
        # Set uri data from Request object.
        if aRequest.protocol.count('HTTPS') > 0: self.protocol = 'https'
        rawIP, self.port = aRequest.connection.local_addr
        self.hostname = aRequest.hostname
        atoms = aRequest.uri.split("/")
        self.script = atoms.pop()
        self.path = "/".join(atoms)
        
        self.user = aRequest.user
        
        # Retrieve the submitted parameters from Apache/mod_python.
        # ONLY CALL ONCE per request.
        newData = util.FieldStorage(aRequest, 1).list
        self.requestParams.flush()
        if newData is not None:
            for eachParam in newData:
                self.requestParams.add_param(str(eachParam.name),
                                             str(eachParam.value))
        
    def write(self, textToOutput):
        self.response.write(textToOutput)



###############################
# D:\htdocs\myapp\dispatch.py #
###############################

from myapp.interface import uimodpython

def handler(req):
    return uimodpython.UserInterfaceModPython(req).dispatch()


#####################
# myapp-apache.conf #
#####################

<Directory D:\htdocs\myapp>
  AddHandler python-program .htm
  PythonHandler dispatch
</Directory>
