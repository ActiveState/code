#!/usr/bin/env python
"""
Usage of threaded.local as gettext() to implement the __builtin__
I18n _() kludge in a multi-threaded environment.  This is a simple
proof-of-concept that demonstrates the kludge.
"""

import threading, time, __builtin__, random


# Create a translator function that can be used in __builtin__ to
# fetch translations from the gettext catalogs and will work in a
# multi-threaded environment. This gets setup once.
catalogs = threading.local()

def gettext_getfunc( lang ):
    """
    Returns a function used to translate to a specific catalog.
    """
    # Note: you would get the gettext catalog here and install it in the
    # closure.

    def tr( s ):
        # Note: we do not really translate here, we just prepend the
        # language, but you get the idea.
        return '[%s] %s' % (lang, s)

    return tr

def gettext_translate( s ):
    """
    Thread-safe version of _().
    We look up the thread-local translation function.
    """
    return catalogs.translate(s)

# Inject the _() function in the builtins.  You could also inject a N_()
# function for noop translation markers.
__builtin__._ = gettext_translate


def handle_request():
    """
    Treat a request, with i18n strings.
    """
    # Fetch and return a translated string.
    # This is the interesting bit, from a client's point-of-view.
    print _('bli'), _('bla'), _('blo')

    # Do something else.
    time.sleep(random.random())


# A thread class.  This would be provided by the web framework,
# normally.
class Thread(threading.Thread):
    def __init__( self, num ):
        threading.Thread.__init__(self)
        self.num = num

    def run( self ):
        while 1: # many requests
            # Setup a request.

            # Get the request's language (we just select a random
            # language here for demonstration purposes).
            reqlang = random.choice(['en', 'fr', 'es', 'de',
                                     'pt', 'si', 'dk', 'it'])

            # Setup current language for thread with a closure that
            # efficiently implement the desired catalog lookup.
            catalogs.translate = gettext_getfunc(reqlang)

            # Dispatch a request to be handled.
            handle_request()


# Create and launch test threads.
threads = []
for x in xrange(5):
    t = Thread(x)
    t.start()
