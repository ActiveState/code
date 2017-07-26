"""
Mini commands - Provides a template for writing quick
command classes in Python using the subprocess module.

Author: Anand B Pillai <abpillai@gmail.com>

"""

import os
import time
from subprocess import *

class CmdProcessor(object):
    """ Class providing useful functions to execute system
    commands using subprocess module """
    
    def execute_command_in_shell(self, command,args=[]):
        
        """ Execute a shell command

        Parameters:

        command - The command to execute
        args    - Command arguments, as a list
        """

        execfn = ' '.join([command] + list(args))
            
        try:
            p = Popen(execfn, env=os.environ, shell=True)
            p.wait()
            return p.returncode
        
        except Exception,e:
            print e
        
        return -1
        
    def execute_command(self, command, args=[]):
        """ Execute a command

        Parameters:

        command - The command to execute
        args    - Command arguments, as a list
        """

        execfn = [command] + list(args)

        try:
            p = Popen(execfn, env=os.environ)
            p.wait()
            return p.returncode
        except Exception,e:
            print e
        
        return -1

    def execute_command_in_pipe(self, command, args=[], estdin=None, estdout=None):
        """ Execute a command by reading/writing input/output from/to optional
        streams like a pipe. After completion, return status """

        execfn = [command] + list(args)

        try:
            in_stream = False
            out_stream = False
            
            # Check if this is a stream
            if hasattr(estdin, 'read'):
                fpin = estdin
                in_stream = True
            elif type(estdin) in (str, unicode):
                fpin = open(estdin, 'r')
                in_stream = True
            if hasattr(estdout, 'write'):
                fpout = estdout
                out_stream = True
            elif type(estdout) in (str, unicode):
                fpout = open(estdout, 'w')
                out_stream = True
                
            if in_stream and out_stream:
                p = Popen(execfn, stdin=fpin, stdout=fpout, stderr=PIPE)
            elif in_stream and not out_stream:
                p = Popen(execfn, stdin=fpin, stdout=PIPE, stderr=PIPE)
            elif not in_stream and out_stream:
                p = Popen(execfn, stdin=PIPE, stdout=fpout, stderr=PIPE)
            elif not in_stream and not out_stream:
                p = Popen(execfn, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            return p.wait()
            
        except Exception,e:
            print str(e)
                
        return -1

class MiniCommand(object):
    """ Base class for mini-commands """

    # This is the original command executed by the class
    command = None
    # Any prefix arguments which will be used by all
    # sub-classes of this class
    prefix_args = []
    # A command template string which can be used
    # to define the skeleton of a command.
    template = ''
    # The base function which can be overridden
    func = 'execute_cmd'
    cmdproc = CmdProcessor()
    
    def __init__(self, command=None, prefix_args=[], template=''):
        if command:
            self.command = command
        if prefix_args:
            self.prefix_args = prefix_args
        if template:
            self.template = template
            
        self.call_func = getattr(self, self.func)

    def __call__(self, *args, **kwargs):

        args = self.prefix_args + list(args)
        if self.template:
            args = self.template % tuple(args)
            # args = args.split()
            print 'ARGS=>',args
            for item in args:
                if item.find('=') != -1:
                    args.remove(item)
                    name, value = item.split('=')
                    kwargs[name] = value

        return self.call_func(*args, **kwargs)

    def execute_cmd(cls, *args, **kwargs):
        return cls.cmdproc.execute_command(cls.command, args, **kwargs)
    
    def execute_shell_cmd(cls, *args, **kwargs):
        return cls.cmdproc.execute_command_in_shell(cls.command, args, **kwargs)
    
    def execute_cmd_in_pipe(cls, *args, **kwargs):
        return cls.cmdproc.execute_command_in_pipe(cls.command, args, **kwargs)
    
    execute_cmd = classmethod(execute_cmd)
    execute_shell_cmd = classmethod(execute_shell_cmd)
    execute_cmd_in_pipe = classmethod(execute_cmd_in_pipe)

# Simple example : ls command
class ListDirCmd(MiniCommand):
    """ This is a sample command added to display functionality """

    if os.name == 'posix':
        command = 'ls'
    elif os.name == 'nt':
        command = 'dir'

    func = 'execute_shell_cmd'
    
class DirTreeCmd(MiniCommand):

    if os.name == 'nt':
        command = 'tree.com'
        
class DeltreeCmd(MiniCommand):
    """ Command to remove a directory tree """
    
    if os.name == 'posix':
        command = 'rm'
        prefix_args = ['-rf']
        
    elif os.name == 'nt':
        command = 'rmdir'
        prefix_args = ['/S','/Q']


    func = 'execute_shell_cmd'

class IPConfigCmd(MiniCommand):
    command  = "ipconfig"

class PythonCmd(MiniCommand):
    command = 'python'

 # Java key-tool command
class JavaKeytoolCommand(MiniCommand):
    """ Class encapsulating java key-tool command """
    command = 'keytool'

class SampleKeystoreGenCmd(JavaKeytoolCommand):
    """ Generate sample key store using key-tool """

    func = 'execute_cmd_in_pipe'
    template = '-genkey -keystore %s -keyalg RSA -alias %s -trustcacerts estdin=%s'
    
if __name__ == '__main__':
    # example: ls command
    lsinst = ListDirCmd()
    lsinst()
    lsinst('-al')

    cmd = IPConfigCmd()
    cmd("/all")

    cmd = PythonCmd()
    cmd()    
    
    try:
        os.makedirs("/tmp/abcd")
        os.makedirs("/tmp/abcd2")
    except os.error, e:
        pass
    
    cmd = DeltreeCmd()
    if os.path.isdir('/tmp/abcd'):
        print cmd('/tmp/abcd')
    if os.path.isdir('/tmp/abcd2'):        
        print cmd('/tmp/abcd2')
