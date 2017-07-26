#!/usr/bin/env python

import traceback
import re
import sys

class CausedException(Exception):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], Exception):
            # we shall just wrap a non-caused exception
            self.stack = (
                traceback.format_stack()[:-2] +
                traceback.format_tb(sys.exc_info()[2]))
            # ^^^ let's hope the information is still there; caller must take
            #     care of this.
            self.wrapped = args[0]
            self.cause = ()
            super(CausedException, self).__init__(repr(args[0]))
            # ^^^ to display what it is wrapping, in case it gets printed or similar
            return
        self.wrapped = None
        self.stack = traceback.format_stack()[:-1]  # cut off current frame
        try:
            cause = kwargs['cause']
            del kwargs['cause']
        except:
            cause = ()
        self.cause = cause if isinstance(cause, tuple) else (cause,)
        super(CausedException, self).__init__(*args, **kwargs)

    def causeTree(self, indentation='  ', alreadyMentionedTree=[]):
        yield "Traceback (most recent call last):\n"
        ellipsed = 0
        for i, line in enumerate(self.stack):
            if (ellipsed is not False and i < len(alreadyMentionedTree) and
                line == alreadyMentionedTree[i]):
                ellipsed += 1
            else:
                if ellipsed:
                    yield "  ... (%d frame%s repeated)\n" % (
                        ellipsed, "" if ellipsed == 1 else "s")
                    ellipsed = False  # marker for "given out"
                yield line
        exc = self if self.wrapped is None else self.wrapped
        for line in traceback.format_exception_only(exc.__class__, exc):
            yield line
        if self.cause:
            yield ("caused by: %d exception%s\n" %
                (len(self.cause), "" if len(self.cause) == 1 else "s"))
            for causePart in self.cause:
                for line in causePart.causeTree(indentation, self.stack):
                    yield re.sub(r'([^\n]*\n)', indentation + r'\1', line)

    def write(self, stream=None, indentation='  '):
        stream = sys.stderr if stream is None else stream 
        for line in self.causeTree(indentation):
            stream.write(line)

if __name__ == '__main__':

    def deeplib(i):
        if i == 3:
            1 / 0  # raise non-caused exception
        else:
            raise CausedException("deeplib error %d" % i)

    def library(i):
        if i == 0:
            return "no problem"
        elif i == 1:
            raise CausedException("lib error one %d" % i)
        elif i == 2:
            try:
                deeplib(i)
            except CausedException, e:
                raise CausedException("lib error two %d" % i, cause=e)
            except Exception, e:  # non-caused exception?
                raise CausedException("lib error two %d" % i,
                    cause=CausedException(e))  # wrap non-caused exception
        elif i == 3:
            try:
                deeplib(i)
            except CausedException, e:
                raise CausedException("lib error three %d" % i, cause=e)
            except Exception, e:  # non-caused exception?
                wrappedException = CausedException(e)  # wrap it for fitting in
                try:
                    deeplib(i-1)  # try again
                except CausedException, e:
                    raise CausedException("lib error three %d" % i,
                        cause=(wrappedException, CausedException(e)))
        else:
            raise CausedException("lib error unexpected %d" % i)

    def application():
        e0 = e1 = e2 = e3 = None
        try: library(0)
        except CausedException, e:  e0 = e
        try: library(1)
        except CausedException, e:  e1 = e
        try: library(2)
        except CausedException, e:  e2 = e
        try: library(3)
        except CausedException, e:  e3 = e
        if e0 or e1 or e2 or e3:
            raise CausedException("application error",
                cause=tuple(e for e in (e0, e1, e2, e3) if e is not None))

    try:
        application()
    except CausedException, e:
        e.write()
        print >>sys.stderr, "NOW WITH MORE OBVIOUS INDENTATION"
        e.write(indentation='||  ')
    print >>sys.stderr, "NOW THE DEFAULT HANDLER"
    application()
