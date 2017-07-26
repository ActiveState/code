#server.py
from SimpleXMLRPCServer import SimpleXMLRPCServer

def export(module):
    exec('import %s as m' % module)
    filename = m.__file__[:-1] #make pyc = py
    return open(filename).read()

server = SimpleXMLRPCServer(('localhost',1979))
server.register_function(export)
server.serve_forever()

#client.py
from xmlrpclib import ServerProxy
import sha

def remoteImport(module):
    """
    Import a module from a remote server.
    Returns a module object.
    """
    server = ServerProxy('http://localhost:1979')
    filename = sha.new(module).hexdigest() #create a temporary filename
    try:
        code = server.export(module)
    except: #if anything goes wrong, try and read from a (possibly) cached file.
        try:
            code = open('%s.py' % filename).read()
        except IOError: #if we don't have a cached file, raise ImportError
            raise ImportError, 'Module %s is not available.' % module
    #dump the code to file, import it and return the module
    open(filename+'.py','w').write(code)
    exec('import %s as m' % filename)
    return m

if __name__ == "__main__":
    m = remoteImport('test')
    print m.add(1,3)

#test.py
def add(a,b):
    return a + b
