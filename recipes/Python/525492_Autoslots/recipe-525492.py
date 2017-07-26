import inspect, _ast
class Autoslots_meta(type):
    """
    Looks for assignments in __init__
    and creates a __slot__ variable for all the
    instance attributes in the assignment.
    Assumes that all assignments in __init__ are of
    the form:
        self.attr = <value>
    """
    def __new__(cls, name, bases, dct):
	slots = dct.get('__slots__', [])
	orig_slots = []
	for base in bases:
	    if hasattr(base, "__slots__"):
		orig_slots += base.__slots__
	if '__init__' in dct:
	    init = dct['__init__']
	    initproc = type.__new__(cls, name, bases, dct)
	    initproc_source = inspect.getsource(initproc)
	    ast = compile(initproc_source, "dont_care", 'exec', _ast.PyCF_ONLY_AST)
	    classdef = ast.body[0]
	    stmts = classdef.body
	    for declaration in stmts:
		if isinstance(declaration, _ast.FunctionDef):
		    name1 = declaration.name
		    if name1 == '__init__': # delete this line if you do not initialize all instance variables in __init__
			initbody = declaration.body
			for statement in initbody:
			    if isinstance(statement, _ast.Assign):
				for target in statement.targets:
				    name1 = target.attr
				    if name1 not in orig_slots:
					slots.append(name1)
	    if slots:
		dct['__slots__'] = slots
	return type.__new__(cls, name, bases, dct)


class Autoslots(object):
    __metaclass__ = Autoslots_meta

class TestClass(Autoslots):
    def __init__(self):
	self.a = 1
	self.b = 2

    def t(self):
	pass
