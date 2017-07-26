#========================= uncertainties.py =========================

"""
Calculations with uncertainties (and correlations): class Number_with_uncert.

Uncertainties are treated like standard deviations.  Valid operations
include basic mathematical functions (addition,...), as well as operations
from the math module.  Logical operations (>, <, etc.) are also supported,
but the calculated error is generally meaningless.

Applying operations on Number_with_uncert creates 'semi-formal'
expressions (see below), represented by the Semi_formal_expr class.

The method used for managing uncertainties consists in replacing
numbers by a kind of mathematical expressions (of type
Semi_formal_expr) that can be calculated for different values of the
variables on which they depend--even if the dependence is not in the
form of an explicit Python function call with some parameters.  These
expressions are 'semi-formal' in the sense that all their parameters
are bound to a value at all times, but they can nonetheless be
recalculated for different values of these parameters.  In particular,
these semi-formal expressions always have a value.

Example:
>>> x = Number_with_uncert(3.14, 0.01)
>>> y = 2*x
>>> print x-x
0.0
>>> print y-x  # The error should be exactly the error on x
3.14 +- 0.010000000000
>>> x.nominal_value = 1
>>> print y  # 'y' is updated
2.0 +- 0.0200000000001

(c) Eric O. LEBIGOT (EOL), 2009.

Strongly inspired by code by Arnaud Delobelle
(http://groups.google.com/group/comp.lang.python/msg/b92987c7787346ec)
"""

__all__ = ["Number_with_uncert"]

###############################################################################

class _Exact_constant(object):
    """
    Expression that represents an exact (no error) constant function.

    Used in wrap_func_output() for a uniform access to expression parts
    (wrap_func_output() expects some attributes from expression parts).
    """
    # This class exists so as not to uselessly create semi-formal variables
    # (Semi_formal_var objects), which are kept in memory.
    def __init__(self, value):
        self._variables = set()
        self.nominal_value = value

def to_func(x):
    """
    Coerces x into a constant expression, unless x is already an
    expression (Semi_formal_expr object).
    """    
    return x if isinstance(x, Semi_formal_expr) else _Exact_constant(x)
    
def wrap_func_output(f):

    """
    Transforms a Python function into an expression that can return
    the result of 'f', but generally as a Semi_formal_expr object
    (unless its evaluation does not involve variables [Semi_formal_var
    objects], in which case 'f' simply returns its usual result).
    """
    
    def f_with_expr_output(*args):
        
        #! The following does not seem to go into the expression returned
        # by wrap_func_output().  Why?
        """
        Version of %s(...) that returns a semi-formal expression
        (Semi_formal_expr object), if its result depends on variables
        (Semi_formal_var objects).  The new version returns a simple
        constant, when applied to constant arguments.
        
        Original documentation:
        %s
        """ % (f.__name__, f.__doc__)
        
        # Coercion of all arguments to semi-formal expressions:
        sub_exprs = map(to_func, args)

        # We keep track of all Semi_formal_var leaves:
        variables = set()
        for sub_expr in sub_exprs:
            variables |= sub_expr._variables

        # Formal version of 'f': its value can be calculated through
        # the specificaton of the values of the variables used in the
        # arguments 'args'.
        def f_evaluation():
            """
            Returns the value of function 'f', calculated at the
            nominal values of its arguments sub_exprs.
            """
            return f(*(sub_expr.nominal_value for sub_expr in sub_exprs))

        if variables:
            # Delayed evaluation:
            return Semi_formal_expr_node(f_evaluation, variables)
        else:
            # Constant functions do not have to be complicated
            # objects:
            return f_evaluation()

    return f_with_expr_output

class Semi_formal_expr(object):

    """
    Semi-formal expression object that supports the mathematical
    operations of Python floats and give objects of the same type
    (Semi_formal_expr).

    Semi_formal_expr objects can thus be summed, etc.

    They are ssentially identical to a mathematical expression
    involving floats, with the difference that it effectively contains
    a way of recalculating its value and adapt to changes in its
    variables.

    The only 'variables' considered in this class are Semi_formal_var
    objects (numbers with an uncertainty).

    Attributes and methods defined through inheritance:

    - (nominal_value, error): nominal (central) value and error on the
      expression.  Before accessing these, no calculation of the
      expression is performed.  These quantities are dynamically
      calculated.

    - derivative_value(variable): value of the partial derivative
      with respect to the given variable (Semi_formal_var object), at
      the point currently defined by the nominal values of the
      variables.
    
    - _variables: semi-formal variables (Semi_formal_var objects) on
      which the expression depends.
    """

    def __repr__(self):
        return "%s object with result %s" % (type(self), str(self))
            
    def __str__(self):
        (nominal_value, error) = self.nominal_value, self.error    
        return ("%s +- %s" % (nominal_value, error) if error
                else str(nominal_value))

    # Conversion to float would be risky: calculations could be
    # performed without error handling, and without the user noticing
    # it.  A number with an uncertainty is not a pure number.  Note
    # that float(1j) is not allowed, for instance.
    def __float__(self):
        raise TypeError("can't convert a number with uncertainty (%s)"
                        " to float; use x.nominal_value"
                        % self.__class__)

    # Operators with no reflection:

    # Logical operators: warning: the resulting value cannot always be
    # differentiated.
    for operator in ('eq', 'ge', 'gt', 'le', 'lt', 'ne'):
        exec ("__%s__ = wrap_func_output(float.__%s__)"
              % (operator, operator))    

    # __nonzero__() is supposed to return a boolean value (it is used
    # by bool()).  It is for instance used for converting the result
    # of comparison operators to a boolean, in sorted().  If we want
    # to be able to sort Semi_formal_expr objects, __nonzero__ cannot
    # return a Semi_formal_expr object.  Since boolean results (such
    # as the result of bool()) don't have a very meaningful
    # uncertainty, this should not be a big deal:
    def __nonzero__(self):
        return bool(self.nominal_value)

    # Operators that return a numerical value:
    for operator in ('abs', 'neg', 'pos'):
        exec ("__%s__ = wrap_func_output(float.__%s__)"
              % (operator, operator))
    
    # Operators with a reflection:
    for operator in ('add', 'div', 'divmod', 'floordiv','mod', 'mul',
                     'pow', 'sub', 'truediv'):
        for prefix in ('', 'r'):
            method_name = "__%s%s__" % (prefix, operator)
            exec("%s = wrap_func_output(float.%s)"
                 % (method_name, method_name))

    del operator, prefix, method_name


class Semi_formal_var(Semi_formal_expr):
    
    """
    Semi-formal variable.

    The variable is bound to a value+uncertainty at all times.

    This is a special kind of semi-formal expression (Semi_formal_expr object),
    with a constant value.
    """
    
    def __init__(self, nominal_value, error = 0):
        
        """
        'nominal_value' is the nominal value of the semi-formal variable.
        'error' is the error on the value.
        """

        # We initialize the value in the same way as users of
        # instances who would set it: users use the 'nominal_value' attribute:
        self.nominal_value = nominal_value  # Defines the (constant) expression
        self.error = error
        # Expression 'x' depends on 'x':
        self._variables = set([self])

    def get_value(self): return self.__nominal_value
    def set_value(self, nominal_value):
        """
        Since evaluations of Semi_formal_expr expression use functions
        that use float arguments, the value of the variables needs to
        be a float.
        """
        self.__nominal_value = float(nominal_value)        
    nominal_value = property(get_value, set_value)
    
    def derivative_value(self, variable, step = 1):
        return 1. if self is variable else 0.

class Semi_formal_expr_node(Semi_formal_expr):
    """
    Semi-formal expression, as defined by a 'regular' Python function.
    """

    def __init__(self, func, variables):
        """
        Node for a semi-formal expression (Semi_formal_expr).
        
        For the meaning of object attributes see the documentation for
        Semi_formal_expr.
        """
        self._evaluate = func  # Way of evaluating the function
        self._variables = variables

    #! It might be numerically more relevant to evaluate at .nominal_value+.err
    # ... but this is not standard.  AND: I'm not sure this would yield
    # a more correct way of estimating the variance (does this take the
    # second order derivative into account??)  THIS WOULD BE USEFUL
    # if .err is a more reasonnable value than step...
    def derivative_value(self, variable, step = 1e-5):
        """
        Calculates the derivative of the expression with respect to
        the given variable (Semi_formal_var object), at the point
        defined by the nominal (central) value of its variables.

        'step' is the numerical variation on 'variable' for the numerical
        calculation of the derivative.  -log10(step) is an estimate of
        the number of digits lost in the derivative calculation.
        """
        
        # Value of the function:
        central_value = self._evaluate()

        # We temporarily shift the value of the variable:
        previous_nominal_value = variable.nominal_value
        variable.nominal_value += step
        new_value = self._evaluate()
        variable.nominal_value = previous_nominal_value
        
        derivative_value = (new_value-central_value)/step
        
        return derivative_value

    @property
    def nominal_value(self):
        """
        Returns the nominal (central) value of the expression, for the
        current nominal value of its variables.
        """
        return self._evaluate()

    @property
    def error(self):
        """
        Returns the error on the expression, at the current nominal
        value of its variables.
        """
        # Caculation of the variance:
        variance = 0
        for variable in self._variables:
            #! This is not efficient: the "central" function value is
            # calculated many times: (an alternative would be to
            # effectively calculate the derivative here)
            value_shift = (self.derivative_value(variable)*variable.error)
            variance += value_shift**2
        error = variance**0.5
        return error

# We wrap the expressions from the math module so that they keep track
# of uncertainties.
BUILTIN_FUNC = type(sum)  # Built-in expression type
import math
for name in dir(math):
    obj = getattr(math, name)
    if isinstance(obj, BUILTIN_FUNC):
        setattr(math, name,  wrap_func_output(obj))

###############################################################################
# Values with uncertainties:
#
Number_with_uncert = Semi_formal_var
###############################################################################
