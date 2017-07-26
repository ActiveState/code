#!/usr/bin/env python
#-*- coding: iso-8859-1 -*-

###############################################################################

class expected:

    def __init__(self, e):
        if isinstance(e, Exception):
            self._t, self._v = e.__class__, str(e)
        elif isinstance(e, type) and issubclass(e, Exception):
            self._t, self._v = e, None
        else:
            raise Exception("usage: with expected(Exception): or with expected(Exception(\"text\"))")

    def __enter__(self):
        try:
            pass
        except:
            pass # this is a Python 3000 way of saying sys.exc_clear()

    def __exit__(self, t, v, tb):
        assert t is not None, "expected {0:s} to have been thrown".format(self._t.__name__)
        return issubclass(t, self._t) and (self._v is None or str(v).startswith(self._v))

###############################################################################

if __name__ == "__main__": # some examples

    try:
        with expected("foo"):
            pass
    except Exception as e:
        assert str(e) == "usage: with expected(Exception): or with expected(Exception(\"text\"))", str(e)
    else:
        assert False

    with expected(ZeroDivisionError):
        1 / 0

    with expected(ZeroDivisionError("int division or modulo by zero")):
        1 / 0

    with expected(ZeroDivisionError("int division")):
        1 / 0

    try:
        with expected(ZeroDivisionError):
            1 / 2
    except AssertionError as e:
        assert str(e) == "expected ZeroDivisionError to have been thrown", str(e)
    else:
        assert False

    try:
        with expected(ZeroDivisionError("failure !!!")):
            1 / 0
    except ZeroDivisionError as e:
        assert str(e) == "int division or modulo by zero", str(e)
    else:
        assert False

    try:
        with expected(ZeroDivisionError):
            {}["foo"]
    except KeyError as e:
        assert str(e) == "'foo'", str(e)
    else:
        assert False

    with expected(KeyError):
        with expected(ZeroDivisionError):
            with expected(RuntimeError):
                {}["foo"]

    with expected(Exception("int division or modulo by zero")):
        1 / 0

    with expected(Exception):
        1 / 0
