import re

def parse_revision_string(r):
    # convert "$Revision: x.y.z $" => "x.y.z"
    try:
        return re.search('Revision: (.*?)\s*\$',r).group(1)
    except:
        return "0"

# PickleRevisionControl class.  Inherit me.
class PickleRevisionControl(object):
    # Important!  This line must be put into all subclasses
    __revision__ = parse_revision_string("$Revision$")

    def __init__(self):
        self.__revision__ = self.__revision__

    def is_obsolete(self):
        return self.__revision__ < self.__class__.__revision__

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.is_obsolete():
            self.upgrade()
            self.__revision__ = self.__class__.__revision__

    def upgrade(self):
        # do your upgrading here.
        pass


#-----------------------------------------------------------------
# Example usage scenario
#-----------------------------------------------------------------
# Suppose you have a class "Widget" in Widget.py.  One day, after a
# little misunderstanding with NASA, you get a memo declaring that 
# all widget measurements will henceforth be in metric units.
#
# Changes to the widget source code go quickly, and you commit Widget.py
# version 1.5 to CVS.  Unfortunately, all of your pickled version 1.4 
# widgets still use imperial units for everything.  But you've been 
# using the PickleRevisionControl class all along, so you can fix 
# things by adding few lines to Widget.upgrade()
#
# 
# class Widget(PickleRevisionControl):
#    __revision__ = parse_revision_string("$Revision: 1.5 $")
#    def __init__(self):
#        PickleRevisionControl.__init__(self)
#        ...
#
#    def upgrade(self):
#        if self.__revision__ < '1.5':
#            self.radius *= 0.0254  # inches to meters
#            self.height *= 0.0254 
#
#    ...
#
# Now your old widgets will be magically updated when you unpickle them!
