import re

class AwkUnhandledLine( RuntimeError ):
    pass

class Awk:
    """awk-like mapping from patterns to handlers."""
    def __init__(self):
        # Start without any patterns
        self.pats=[]
    def add(self,pattern,handler=None):
        # Add a pattern and its handler,
        # precompiling the pattern
        self.pats.append((re.compile(pattern),handler))
    def process(self,line):
        # Find the first pattern that matches the input,
        # and call the handler with the result of the match.
        for pat, handler in self.pats:
            m = pat.match(line)
            if m:
                if callable(handler):
                    return handler(**m.groupdict())
                else:
                    return handler
        raise AwkUnhandledLine( line )

class AwkFileInput(Awk):
    def __init__(self):
        import fileinput
        self.fileinput = fileinput
        Awk.__init__(self)
    def processinput(self):
        for line in self.fileinput.input():
            try:
                self.process(line)
            except AwkUnhandledLine, e:
                raise AwkUnhandledLine(
                    "Don't understand line %d of file %s: %s" %
                    (fileinput.filelineno(),
                     fileinput.filename(),
                     line) )

# example:

def handle_thing(name=None,num=0):
    if name:
        print name, "=", float(num)
    else:
        print float(num), "has no name"

def example():
    a = AwkFileInput()
    a.add("^#") # Ignore comments (handler==None)
    a.add("^(?P<num>\d+\.\d+)", handle_thing) # Print numbers
    a.add("^(?P<name>\w+)\s+(?P<num>\d+)", handle_thing) # Print named numbers
    a.processinput()
