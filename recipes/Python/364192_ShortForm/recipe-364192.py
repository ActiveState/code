#Written by Jesse Weinstein <jessw@netwood.net>.
#Released under the Python license on Sat Jan 22 02:56:11 2005.
#shortForm.py
#Short Form prevents the Python shell from printing out giant piles of text.
#Python version: er, 2.3 and later.  Or maybe earlier versions...
#http://www.netwood.net/usr/jessw
#Possible categories: Utilities, Python shell hacks
#First release.
#Released to Useless Python (http://www.uselesspython.com), Vaults of Parnassus,
#  ASPN Python Cookbook, and my site.
"""Short Form prevents the Python shell from printing out giant piles of text.

It is a hack that ties into the display system.  When you are working with a multi-megabyte text file,
referenced under the name `txt`, which takes 10 minutes to be printed in full (if you accidentally
type '>>> txt') it's really nice to have this.

Besides actually turning it off, it can be evaded by using `print` or even sys.stdout.write itself.
ShortForm is only used when an object is repr'ed and printed."""
import sys
def toggle_ShortForm():
    """Toggle the shortening of output."""
    if sys.displayhook==shortForm:
        off()
    else:
        on()
def install(max_size=100, size=30):
    """Use this to start up ShortForm.

    max_size is the maximum length the repr can be before it's shortened.
    size is the length of the beginning and end which is printed.  The total length of a shorted item is
    size*2+3.  The +3 is for the elipsis."""
    sys.shortFormMaxSize=max_size
    sys.shortFormSize=size
    __builtins__['sft']=toggle_ShortForm
def on():
    "Turn on ShortForm."""
    if 'shortFormSize' not in dir(sys):
        install()
    sys.displayhook=shortForm
def off():
    """Turn off ShortForm."""
    sys.displayhook=sys.__displayhook__
def remove():
    """Remove the items ShortForm places in the `sys` namespace."""
    del sys.shortFormMaxSize
    del sys.shortFormSize
    del __builtins__['sft']

def shortForm(item):
    """Write out a shortened form of the provided item."""
    if item is None:
        return
    r=repr(item)
    if len(r) > sys.shortFormMaxSize:
        sys.stdout.write(r[:sys.shortFormSize]+' ... '+\
                         r[-sys.shortFormSize:]+'\n')
    else:
        sys.stdout.write(r+'\n')
