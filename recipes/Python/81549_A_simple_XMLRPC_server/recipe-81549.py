# Server code

import SimpleXMLRPCServer

class StringFunctions:
    def __init__(self):
        # Make all of the Python string functions available through
        # python_string.func_name
        import string
        self.python_string = string

    def _privateFunction(self):
        # This function cannot be called through XML-RPC because it
        # starts with an '_'
        pass
    
    def chop_in_half(self, astr):
        return astr[:len(astr)/2]

    def repeat(self, astr, times):
        return astr * times
    
server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(StringFunctions())
server.register_function(lambda astr: '_' + astr, '_string')
server.serve_forever()

# Client code

import xmlrpclib

server = xmlrpclib.Server('http://localhost:8000')
print server.chop_in_half('I am a confidant guy')
print server.repeat('Repetition is the key to learning!\n', 5)
print server._string('<= underscore')
print server.python_string.join(['I', 'like it!'], " don't ")
print server._privateFunction() # Will throw an exception
