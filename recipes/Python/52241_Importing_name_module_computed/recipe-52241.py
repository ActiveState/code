def importName(modulename, name):
    """ Import a named object from a module in the context of this function,
        which means you should use fully qualified module paths.

        Return None on failure.
    """
    try:
        module = __import__(modulename, globals(), locals(), [name])
    except ImportError:
        return None
        
    return vars(module)[name]

### MyApp/extensions/spam.py
class Handler:
    def handleSomething(self):
        print "spam!"

### MyApp/extensions/eggs.py
class Handler:
    def handleSomething(self):
        print "eggs!"

### Example
extension_name = "spam" # could be "eggs", too!
Handler = importName("MyApp.extensions." + extension_name, "Handler")
handler = Handler()
handler.handleSomething()
