"""Forward processing to a new screen."""

__docformat__ = "restructuredtext"


def forward(self, screen, *args, **kargs):
    """Forward processing to a new screen.  This method does not return.

    Generate a ``Forward`` exception which
    aquarium.util.Aquarium.screenLoop_ class is prepared to catch.

    screen
      This is the module name of the screen relative to the screen
      directory.

    ``*args``, ``**kargs``
      The arguments to pass to the screen's ``__call__`` method.

    .. _aquarium.util.Aquarium.screenLoop: 
        aquarium.util.Aquarium.Aquarium-class.html#screenLoop

    """
    raise Forward(screen, *args, **kargs)


class Forward(Exception):
    
    """Raise an instance of this class to make Aquarium do a forward.

    Actually, you should use aquarium.util.InternalLibrary.forward_ to do that
    for you.

    The following attributes are used:

    screen
      The module name of the screen relative to the ``screen`` directory
    ``*args``, ``**kargs``
      The arguments to pass to the screen's ``__call__`` method.

    .. _aquarium.util.InternalLibrary.forward: 
       aquarium.util.InternalLibrary.InternalLibrary-class.html#forward

    """

    def __init__(self, screen, *args, **kargs):
        """Just accept the parameters."""
        Exception.__init__(self)
        self.screen = screen
        self.args = args
        self.kargs = kargs


def screenLoop(self):
    """Show the desired screen, and loop around to handle exceptions.

    By using a loop, the same code path can be used for exceptions.  In 
    fact:

    * The aquarium.util.InternalLibrary.Forward_ exception results in 
      looping around to show the desired screen to forward to.

    * ``ImportError``'s and ``AttributeError``'s while trying to import the
      screen result in the ``not_found`` screen.

    * Any other ``Exception`` results in the ``exception`` screen.
    
    Be especially wary of infinite loops since we're catching all
    exceptions and looping around.  Use ``handleDoubleException`` in these
    cases, but note that it too will raise an exception, by design.

    If a screen runs successfully to completion, call
    ``self._ctx.dba.commit()`` and return whatever the screen returns.

    .. _aquarium.util.InternalLibrary.Forward: 
       aquarium.util.InternalLibrary.Forward-class.html

    """
    from InternalLibrary import Forward
    class _Continue(Exception): pass    # Can't use continue in an except.
    MAX_FORWARDS = 1024
    ctx = self._ctx
    if hasattr(ctx, "screen"):          # We had an exception in initAll.
        screen, args, kargs = ctx.screen, ctx.args, ctx.kargs
    else:
        screen, args, kargs = ctx.url.whichScreen(), (), {}
    self._prevExc, self._prevExcInfo = None, None
    if not screen:
        screen = properties.DEFAULT_SCREEN
    if not ctx.iLib.validModuleName(screen):
        screen, args, kargs = "not_found", (screen,), {}
    for _ignored in xrange(MAX_FORWARDS):
        try:
            ctx.screen = screen
            try:
                ctx.screenInstance = ctx.iLib.aquariumFactory(
                    "screen." + screen)
            except (ImportError, AttributeError), e:
                self.catchDoubleException(e)
                screen, args, kargs = "not_found", (e), {}
                raise _Continue
            buf = ctx.iLib.inverseExtend(ctx.screenInstance.__call__, 
                                         *args, **kargs)
            if properties.USE_DATABASE: 
                ctx.dba.commit()
            return buf
        except _Continue:
            pass
        except Forward, e:
            screen, args, kargs = e.screen, e.args, e.kargs
        except Exception, e:
            self.catchDoubleException(e)
            screen, args, kargs = "exception", (exc_info(),), {}
    raise OverflowError("Too many forwards")
