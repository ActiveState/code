"""It's a convenient way to deeply nest try/finally statements."""

__docformat__ = "restructuredtext"

from traceback import print_exc


def tryFinally(tasks, handleFinallyException=None):

    """This is a convenient way to deeply nest try/finally statements.

    It is appropriate for complicated resource initialization and destruction.
    For instance, if you have a list of 50 things that need to get intialized
    and later destructed via using try/finally (especially if you need to
    create the list dynamically) this function is appropriate.

    Given::

        tasks = [
            ((f_enter_0, enter_0_args, enter_0_kargs),
             (f_exit_0, exit_0_args, exit_0_kargs)),

            ((f_enter_1, enter_1_args, enter_1_kargs),
             (f_exit_1, exit_1_args, exit_1_kargs)),

            ((f_enter_2, enter_2_args, enter_2_kargs),
             (f_exit_2, exit_2_args, exit_2_kargs))
        ]

    Execute::

        f_enter_0(*enter_0_args, **enter_0_kargs)
        try:

            f_enter_1(*enter_1_args, **enter_1_kargs)
            try:

                f_enter_2(*enter_2_args, **enter_2_kargs)
                try:

                    pass

                finally:
                    try:    
                        f_exit_2(*exit_2_args, **exit_2_kargs)
                    except Exception, e:
                        handleFinallyException(e)

            finally:
                try:    
                    f_exit_1(*exit_1_args, **exit_1_kargs)
                except Exception, e:
                    handleFinallyException(e)

        finally:
            try:    
                f_exit_0(*exit_0_args, **exit_0_kargs)
            except Exception, e:
                handleFinallyException(e)

    tasks
        See the example above.  Note that you can leave out parts of the tuples
        by passing shorter tuples.  For instance, here are two examples::

            # Second tuple missing.
            ((f_enter_2, enter_2_args, enter_2_kargs),)

            # Leave out args or args and kargs.
            ((f_enter_2,),
             (f_exit_2, exit_2_args))

        Don't forget that a tuple of 1 item is written ``(item,)``.  This is an
        amazingly easy thing to do.

    handleFinallyException(e)
        This is a callback that gets called if an exception, ``e``, is raised
        in a finally block.  By default, traceback.print_exc is called.

    """

    def defaultFinallyExceptionHandler(e):
        print_exc()

    def castTwoParts(first):
        lenFirst = len(first)
        default = ((), ())
        max = len(default)
        if lenFirst > max:
            raise ValueError("""\
tasks must be a list of tuples of the form (enterTuple, exitTuple).""", first)
        return first + default[lenFirst:]

    def doNothing(*args, **kargs):
        pass

    def castFunctionArgsKargs(fTuple):
        lenFTuple = len(fTuple)
        default = (doNothing, (), {})
        max = len(default)
        if lenFTuple > max:
            raise ValueError("""\
Each tuple in tasks is a pair of tuples that look like (f, args, kargs).""",
                             fTuple)
        return fTuple + default[lenFTuple:]

    if not len(tasks):
        return
    if not handleFinallyException:
        handleFinallyException = defaultFinallyExceptionHandler

    first, others = tasks[0], tasks[1:]
    first = castTwoParts(first)
    first = (castFunctionArgsKargs(first[0]),
             castFunctionArgsKargs(first[1]))
    ((fEnter, fEnterArgs, fEnterKargs),
     (fExit, fExitArgs, fExitKargs)) = first

    fEnter(*fEnterArgs, **fEnterKargs)
    try:
        tryFinally(others, handleFinallyException)
    finally:
        try:
            fExit(*fExitArgs, **fExitKargs)
        except Exception, e:
            handleFinallyException(e)


if __name__ == '__main__':

    from cStringIO import StringIO

    def printEverything(*args, **kargs): print >>buf, `args`, `kargs`
    def refuseArgs(): print >>buf, "refused args"
    def raiseValueError(): raise ValueError
    def finallyExceptionHandler(e): print >>buf, "caught exception in finally"

    tasks = [
        ((printEverything, ("enter_0_args",), {"in": "in"}),
         (printEverything, ("exit_0_args",))),

        ((printEverything,),
         (raiseValueError,)),

        ((refuseArgs,),)
    ]

    result = """\
('enter_0_args',) {'in': 'in'}
() {}
refused args
caught exception in finally
('exit_0_args',) {}
"""

    buf = StringIO()
    tryFinally(tasks, finallyExceptionHandler)
    assert buf.getvalue() == result
