import sys,re,time
import pexpect
import exceptions

from string import *
from telnetlib import Telnet

""" Define exceptions """

class TelnetError(exceptions.Exception):
    def __init__(self, args=None):
        self.args=args
        self.errmsg = ''
        for a in self.args:
            self.errmsg += str(a)

class JumpError(exceptions.Exception):
    def __init__(self, args=None):
        self.args=args
        self.errmsg = ''
        for a in self.args:
            self.errmsg += str(a)

class Jump:

    """ Initiate an SSH tunnel  
    """
    def __init__(self, host, env = {}):

        """ If env not passed explicitly, then 
            assume that its inherited from parent 
            class.
        """
        if env != {}:
           self.env = env

        self._jump_params()

        sshcmd = "ssh %s -L %s:%s:23" % \
            (self.jumpserver,self.jumpport,host)

        if self.DEBUG >= 3: print "ssh cmd: %s" % (sshcmd)

        """ Create SSH tunnel """
        self.tunnel = pexpect.spawn(sshcmd)

        if self.DEBUG >= 2: print "jump to %s:%s" % \
                (self.jumpserver,self.jumpport)

        if self.DEBUG >= 3: print "waiting for %s" % \
            (self.jumpprompt)

        """ Process response from jump server """
        expected_replies = [self.jumpprompt,\
            'Are you sure you want to continue connecting'\
            'ssword:']

        while 1:
            response = self.tunnel.expect(expected_replies)

            if response == 0:  # got prompt
                break

            """ Got ssh password, prompt, so no public 
                key encryption set up
            """
            if response == 1:  
                if self.env.has_key('SSHPASSWD'):
                    self.sshpassword = "%s\n" % \
                        (self.env['SSHPASSWD'])
                else:
                    raise JumpError, "no SSH Password"
                self._ssh_login()

            """ If prompted, add to known_hosts file """
            if response == 2:               
                self.tunnel.send("yes\n") 
     
        if self.DEBUG >= 1: print self.tunnel.before

        if self.DEBUG >= 3: print "tunnel %s:%s established" % \
                (self.jumpserver,self.jumpport)

    """ Process parameters needed to create the
        SSH tunnel to the Jump host
    """
    def _jump_params(self):

        """ Set debug level """
        if self.env.has_key('DEBUG'):
            self.DEBUG = int(self.env['DEBUG'])
        else:
            self.DEBUG = 0

        try:
            self.jumpserver = self.env['JMPSERVER']
            self.jumpport   = self.env['PORT']
            self.jumpprompt = self.env['JMPPROMPT']
        except:
            raise JumpError, "missing parameters"

        return 0

    """ Login with SSH password
    """
    def _ssh_login(self):
        if self.DEBUG >= 1: print self.tunnel.before
        self.tunnel.send(self.sshpassword)

class Climgmt(Jump):

    def __init__(self,host,env = {}):

        self.host = host

        """ If no environment passed as a parameter,
            then assume environment is inherited from
            parent class. 
        """
        if env != {}:
            self.env = env

        self._climgmt_params()

        """ Create ssh tunnel is jump server specified """
        if self.jumpserver != None:
            Jump.__init__(self,host)  

        if self.DEBUG >= 3: print "Telneting to %s on port %d" %  \
            (self.host, self.port)

        """ Initiate Telnet session """
        try:
            self.session = Telnet(self.host, self.port)
        except: 
            self.tunnel.close()
            raise TelnetError, "cannot establish telnet session"

    """ Set parameters 
    """
    def _climgmt_params(self):

        """ Debug level """
        if self.env.has_key('DEBUG'):
            self.DEBUG = int(self.env['DEBUG'])
        else:
            self.DEBUG = 0

        """ Device prompt """
        if self.env.has_key('PROMPT'):
            self.prompt = self.env['PROMPT'] 
        else:
            self.prommpt = None

        """ Jump server """
        if self.env.has_key('JMPSERVER'):
            self.jumpserver = self.env['JMPSERVER']
            self.host = "localhost"
        else:
            self.jumpserver = None

        """ The Telnet port maybe different because we are 
            going through a jump server (ssh tunnel).
        """
        if self.env.has_key('PORT'):
            self.port = int(self.env['PORT'])
        else:
            self.port = 23    # default Telnet port

        return 0

    """ Issue a command to the Telnet device  
    """
    def cmd(self, cmd, newprompt = None):

        if newprompt == None:
            prompt = self.prompt
        else:
            prompt = newprompt

        self.session.write(cmd+'\n')

        response = self.session.read_until(prompt,8)

        if self.DEBUG >= 3: print response

        lines = response.split('\n')
        lines = map(lambda i: strip(strip(i,'\r')), lines)

        return lines

    """ Close telnet session (and ssh tunnel)   
    """
    def close(self):

        if self.DEBUG >= 3: print "closing Telnet session <%s,%d>" % \
                (self.host, self.port)

        """ Close Telnet session """
        self.session.close()    # close telnet session

        """ Check to see if tunnel exists (note: must 
            find better way of check if tunnel exists) 
        """
        try:
            tunnel_exists = self.tunnel
        except AttributeError, e:
            return -1
        except NameError, e:
            return -1

        if self.DEBUG >= 3: print "closing ssh tunnel <%s,%s>" % \
                (self.jumpserver, self.jumpport)

        """ Close ssh tunnel (if it exists) """
        self.tunnel.close() # close tunnel 
