class Thing(object):
    """A thing, does stuff."""
    def __init__(self):
        self.special = "My special value!"

    def process(self, default=True):
        """Accept any argument with no special processing (except True)."""
        if default is True: # Notice I'm checking identity, not truth or equality
            default = self.special
        elif not default: # Optional check for False values
            print "Non-value given!"
        print default

if __name__ == "__main__":
    t = Thing()
    t.process()            # Prints t's special value
    t.process("something") # Prints 'something'
    t.process(None)        # Prints the False value warning
