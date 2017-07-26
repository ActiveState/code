from __future__ import with_statement
from contextlib import contextmanager
import sys

__docformat__ = "restructuredtext"


@contextmanager
def restoring(expr, clone=None):
    '''A context manager that evaluates an expression when entering the runtime
    context and restores its value when exiting.
    
    This context manager makes
    
    .. python::
        with restoring(expr, clone) as value:
            BODY        
    
    a shortcut for
    
    .. python::
        value = EXPR
        __cloned = clone(value) if clone is not None else value
        try:
            BODY
        finally:
            EXPR = __cloned
            del __cloned
    
    where ``__cloned`` is a temporary hidden name and ``EXPR`` is ``expr``
    substituted textually in the code snippet. Therefore ``expr`` can only be an
    assignable expression, i.e. an expression that is allowed on the left hand
    side of '=' (e.g. identifier, subscription, attribute reference, etc.).
        
    :param expr: The expression whose value is to be evaluated and restored.
    :type expr: str
    :param clone: A callable that takes the object ``expr`` evaluates to and
        returns an appropriate copy to be used for restoring. If None, the
        original object is used.        
    :type clone: callable or None
    '''
    f = sys._getframe(2)    # bypass the contextmanager frame
    # evaluate the expression and make a clone of the value to be restored
    value = eval(expr, f.f_globals, f.f_locals)
    restored_value = clone(value) if clone is not None else value
    try:
        yield value
    finally:
        if expr in f.f_locals:      # local or nonlocal name
            _update_locals(f, {expr:restored_value})
        elif expr in f.f_globals:   # global name
            f.f_globals[expr] = restored_value
        else:
            # make a copy of f_locals and bind restored_value to a new name
            tmp_locals = dict(f.f_locals)
            tmp_name = '__' + min(tmp_locals)
            tmp_locals[tmp_name] = restored_value
            exec '%s = %s' % (expr, tmp_name) in f.f_globals, tmp_locals


def _update_locals(frame, new_locals, clear=False):
    # XXX: obscure, most likely implementation-dependent fact:
    # f_locals can be modified (only?) from within a trace function
    f_trace = frame.f_trace
    try:
        sys_trace = sys.gettrace()
    except AttributeError: # sys.gettrace() not available before 2.6
        sys_trace = None
    def update_tracer(frm, event, arg):
        # Update the frame's locals and restore both the local and the system's
        #trace function
        assert frm is frame
        if clear:
            frm.f_locals.clear()
        frm.f_locals.update(new_locals)
        frm.f_trace = f_trace
        sys.settrace(sys_trace)
    # Force tracing on with setting the global tracing function and set
    # the frame's local trace function
    sys.settrace(lambda frame, event, arg: None)
    frame.f_trace = update_tracer


def test_restoring_immutable():
    x = 'b'
    foo = {'a':3, 'b':4}
    with restoring('foo[x]') as y:
        assert y == foo[x] == 4
        foo[x] = y = None
        assert y == foo[x] == None
    assert foo[x] == 4 and y == None 
    assert sorted(locals()) == ['foo', 'x', 'y']

def test_restoring_mutable():
    orig_path = sys.path[:]
    with restoring('sys.path', clone=list) as path: 
        assert path is sys.path
        path += ['foo']
        assert path == orig_path + ['foo']
    assert sys.path == orig_path 
    assert path == orig_path + ['foo']
    assert sorted(locals()) == ['orig_path', 'path']

x = 1
def test_restoring_global():
    global y; y = 2
    global x
    with restoring('x'):
        x = None
        with restoring('y'):
            y += 3
            assert x == None and y == 5 
        assert y == 2
    assert x == 1
    assert not locals()

def test_restoring_local():
    x = 5
    with restoring('x'):
        x = None
    assert x == 5
    assert sorted(locals()) == ['x']

def test_restoring_nonlocal():
    a = []
    def nested():
        with restoring('a', list):
            a.append(1)
            assert a == [1]
        assert a == []
    nested()
    assert a == []


if __name__ == '__main__':
    test_restoring_immutable()
    test_restoring_mutable()
    test_restoring_global()
    test_restoring_local()
    test_restoring_nonlocal()
