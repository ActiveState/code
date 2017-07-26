#!/usr/bin/env python
# Copyright (c) 2010-2011 Jan Kaliszewski (zuo). All rights reserved.
# Licensed under the MIT License. Python 2.6/2.7-compatibile.

import os.path
import sys
from contextlib import contextmanager
from repr import repr as default_reprfunc

__all__ = 'trace_logging_on',

default_refdir = os.path.dirname(sys.modules['__main__'].__file__)


def trace_logging_on(refdir=default_refdir,    # reference-point directory path
                     negprefix=('..', '<'),  # negative filtering path prefixes
                     filterfunc=(lambda s: True),   # custom filtering function
                     filterarg='',     # .format()-able filter argument pattern
                                       # e.g. '{event}&{path}&{frame.f_lineno}'
                     events2log = { # mapping events to .format()-able log patt
                         'call': '[C  ] {path}: {name}{callargs}',
                         'return': '[  R] {path}: {name}  ->  {argrepr}',
                         'exception': '[ E ] {path}, in {name}:\n{traceback}',
                     },  # [.format()-able patterns refer to tracer()'s locals]
                     logger='',                       # logger name or instance
                     loggermethod='debug',                 # logger method name
                     reprfunc=default_reprfunc):  # repr()-replacement function

    """
    Enable logging of Python call/return/exception events (handily filtered).

    Usage variants:
    * simply-turn-on call:        trace_logging_on(...)
    * context manager syntax:     with trace_logging_on(...): ...
    * context manager with 'as':  with trace_logging_on(...) as tracefunc: ...
    """

    from inspect import getargvalues, formatargvalues
    from traceback import format_exception
    if isinstance(logger, basestring):
        from logging import getLogger
        logger = getLogger(logger)
    log = getattr(logger, loggermethod)
    relpath = os.path.relpath
    formatvalue = (lambda s: '=' + reprfunc(s))
    filterarg_format = filterarg.format

    def tracer(frame, event, arg):
        if event not in events2log:  # initial event filtering
            return tracer
        path = relpath(frame.f_code.co_filename, refdir)  # relative to refdir
        # path-prefix-based scope filtering (negative, i.e. False lets by)
        if path.startswith(negprefix):
            return None  # (<- None to discontinue tracing in sub-scopes)
        # adding some locals (to be used to format filtering/logging arguments)
        name = frame.f_code.co_name
        argrepr = reprfunc(arg)
        if event == 'call':
            argvalues = (getargvalues(frame) if name != '<genexpr>'
                         else ([],) + getargvalues(frame)[1:])
            callargs = formatargvalues(*argvalues, formatvalue=formatvalue)
        elif event == 'exception':
            traceback = ''.join(format_exception(*arg))
        pattern_fields = locals()
        # callback-based individual filtering (positive, i.e. True lets by)
        if not filterfunc(filterarg_format(**pattern_fields)):
            return tracer
        # event-specific logging
        log(events2log[event].format(**pattern_fields))
        return tracer

    with_support = [_with_statement_support(tracer, previous=sys.gettrace())]
    sys.settrace(tracer)
    return with_support.pop()   # (we don't like circular references...)


@contextmanager
def _with_statement_support(tracer, previous):
    yield tracer
    sys.settrace(previous)


if __name__ == '__main__':

    ## Example script ##

    import logging
    from operator import methodcaller

    def robin(a, b, c):
        return c, b, a

    def lancelot(x, y="Let's not bicker and argue", z="about who killed who."):
        return x, y, z

    def rabbit():
        return 1 / 0

    def arthur(nee):
        lancelot('Camelot!')
        robin('Oh, shut up', 'and go', 'and change your armor!')
        robin(*lancelot("Why doesn't Lancelot go?"))
        try:
            rabbit()
        except:
            lancelot(*robin('spam', 'spam', 'spam'))
        return nee

    # enjoy your stderr :)

    logging.basicConfig(level=logging.DEBUG)
    arthur(0)  # (<- not logged)
    with trace_logging_on(logger='tim.the.enchanter',
                          reprfunc='.:{0}:.'.format):
        arthur(1)
        with trace_logging_on(refdir='/usr', negprefix=(),  # any prefix is ok
                              filterarg='{event}', filterfunc='call'.__eq__):
            arthur('2 sheds')
        arthur(3)
    arthur(4)  # (<- not logged)
    trace_logging_on(filterarg='{name}',
                     filterfunc=methodcaller('startswith', 'r'),
                     logger='comfy.chair', loggermethod='info', reprfunc=repr)
    arthur(5)
