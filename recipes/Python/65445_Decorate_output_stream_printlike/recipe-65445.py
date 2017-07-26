class PrintDecorator:
    """Add print-like methods to any file-like object."""

    def __init__(self, stream):
        """Store away the stream for later use."""
        self.stream = stream

    def Print(self, *args, **kw):
        """ Print all arguments as strings, separated by spaces.

            Take an optional "delim" keyword parameter, to change the
            delimiting character.
        """
        delim = kw.get('delim', ' ')
        self.stream.write(delim.join(map(str, args)))

    def PrintLn(self, *args, **kw):
        """ Just like print(), but additionally print a linefeed.
        """
        self.Print(*args+('\n',), **kw)

import sys
out = PrintDecorator(sys.stdout)
out.PrintLn(1, "+", 1, "is", 1+1)
out.Print("Words", "Smashed", "Together", delim='')
out.PrintLn()
