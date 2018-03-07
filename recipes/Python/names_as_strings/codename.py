# MIT License
#
# Copyright (c) 2018 João Ferreira
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dis import Bytecode as _Bytecode
from itertools import takewhile as _takewhile, dropwhile as _dropwhile
from types import CodeType as _CodeType

__all__ = ['name_of']

_ATTR = 'LOAD_ATTR'
_LOAD = (
    _ATTR,
    'LOAD_CLASSDEREF',
    'LOAD_CLOSURE',
    'LOAD_CONST',
    'LOAD_DEREF',
    'LOAD_FAST',
    'LOAD_GLOBAL',
    'LOAD_NAME'
)
_no_value = object()


class _TraceError(Exception):
    """To trace a frame from exception object."""


class _Scopes:
    """Hold mapping: code ids to known scopes."""
    known = {}


def _dis_f(code):
    """Return iterator for a frame's bytecode."""
    return iter(_Bytecode(code))


def _known():
    """Cache and get names from scope's cache."""

    def scope():
        names = scope.cached[scope.no]
        if len(names) == 1:
            return names[0]
        return names.copy()

    scope.cached = []
    scope.no = 0
    return scope


def _not_eq(instruction):
    """Assert argrepr doesn't equal func name."""
    return instruction.argrepr != name_of.__name__


def _eq(instruction):
    """Assert opname equals load an attribute."""
    return instruction.opname == _ATTR


def _iter(instructions):
    """Extract basename of attrs/name of vars."""
    known = None
    for instruction in instructions:
        if not _eq(instruction) and known is not None:
            yield known
        known = instruction.argrepr
    yield known


def _in_load(instruction):
    """Assert opname is found in global _LOAD."""
    return instruction.opname in _LOAD


def _filter(instructions):
    """Return valid identifiers from argument."""
    it = _iter(_takewhile(_in_load, instructions))
    return filter(str.isidentifier, it)


def _cache(bytecode, scope):
    """Extract + cache names from code object."""
    while True:
        instructions = _dropwhile(_not_eq, bytecode)
        if next(instructions, None) is None:
            break
        instructions = list(_filter(instructions))
        scope.cached.append(instructions)


def _pos(code_id, scope):
    """Del scope if its no + 1 exceeds cached."""
    scope.no += 1
    if scope.no == len(scope.cached):
        del _Scopes.known[code_id]


def _name_of(code):
    """Handle known scopes + advance position."""
    code_id = id(code)
    if code_id not in _Scopes.known:
        bytecode = _dis_f(code)
        scope = _Scopes.known[code_id] = _known()
        _cache(bytecode, scope)
    else:
        scope = _Scopes.known[code_id]
    names = scope()
    _pos(code_id, scope)
    return names


def _trace(exc):
    """Return the calling frame's code object."""
    return exc.__traceback__.tb_frame.f_back.f_code


def _invalidate(code):
    """Did not pass CodeType, raise TypeError."""
    raise TypeError('{!r} is not CodeType'.format(code))


def name_of(_, *, code=_no_value):
    """Dig up variable names from code object."""
    if code is _no_value:
        try:
            raise _TraceError
        except _TraceError as exc:
            return _name_of(_trace(exc))
    elif isinstance(code, _CodeType):
        return _name_of(code)
    _invalidate(code)


if __name__ == '__main__':
    x = y = z = var = None


    def _names():
        """Call to be accessed in other scope."""
        name_of((x, y, z))


    def test_filter():
        """Test against an invalid identifier."""
        assert name_of('None') == []


    def test_call_f():
        """Test interruption by function call."""

        def f(_):
            pass

        f.f = f
        assert name_of((f.f(x), y, z)) == ['f', 'x']


    def test_invalidate():
        """Test against non-CodeType argument."""
        try:
            name_of(None, **{'code': 'None'})
        except TypeError:
            pass
        else:
            raise AssertionError


    def test_x_scope():
        """Test cross-scope and multiple vars."""
        code = {'code': _names.__code__}
        assert name_of(None, **code) == 'x y z'.split()


    def test_simple():
        """Test the simplest cases: var, attr."""
        assert name_of(var) == 'var'
        assert name_of(_Scopes.known) == 'known'


    def test_all(*tests):
        """Run tests and assert known cleared."""
        for f in tests:
            f()
        assert _Scopes.known == {}


    test_all(
        test_filter,
        test_call_f,
        test_invalidate,
        test_x_scope,
        test_simple
    )
