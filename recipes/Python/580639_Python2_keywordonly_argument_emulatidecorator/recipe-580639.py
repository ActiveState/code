#!/usr/bin/env python
import inspect
import sys

# The @decorator syntax is available since python2.4 and we support even this old version. Unfortunately functools
# has been introduced only in python2.5 so we have to emulate functools.update_wrapper() under python2.4.
try:
    from functools import update_wrapper
except ImportError:
    def update_wrapper(wrapper, wrapped):
        for attr_name in ('__module__', '__name__', '__doc__'):
            attr_value = getattr(wrapped, attr_name, None)
            if attr_value is not None:
                setattr(wrapper, attr_name, attr_value)
        wrapper.__dict__.update(getattr(wrapped, '__dict__', {}))
        return wrapper


KWONLY_REQUIRED = ('KWONLY_REQUIRED',)
FIRST_DEFAULT_ARG = ('FIRST_DEFAULT_ARG',)


def first_kwonly_arg(name):
    """ Emulates keyword-only arguments under python2. Works with both python2 and python3.
    With this decorator you can convert all or some of the default arguments of your function
    into kwonly arguments. Use ``KWONLY_REQUIRED`` as the default value of required kwonly args.

    :param name: The name of the first default argument to be treated as a keyword-only argument. This default
    argument along with all default arguments that follow this one will be treated as keyword only arguments.

    You can also pass here the ``FIRST_DEFAULT_ARG`` constant in order to select the first default argument. This
    way you turn all default arguments into keyword-only arguments. As a shortcut you can use the
    ``@kwonly_defaults`` decorator (without any parameters) instead of ``@first_kwonly_arg(FIRST_DEFAULT_ARG)``.

        >>> from kwonly_args import first_kwonly_arg, KWONLY_REQUIRED, FIRST_DEFAULT_ARG, kwonly_defaults
        >>>
        >>> # this decoration converts the ``d1`` and ``d2`` default args into kwonly args
        >>> @first_kwonly_arg('d1')
        >>> def func(a0, a1, d0='d0', d1='d1', d2='d2', *args, **kwargs):
        >>>     print(a0, a1, d0, d1, d2, args, kwargs)
        >>>
        >>> func(0, 1, 2, 3, 4)
        0 1 2 d1 d2 (3, 4) {}
        >>>
        >>> func(0, 1, 2, 3, 4, d2='my_param')
        0 1 2 d1 my_param (3, 4) {}
        >>>
        >>> # d0 is an optional deyword argument, d1 is required
        >>> def func(d0='d0', d1=KWONLY_REQUIRED):
        >>>     print(d0, d1)
        >>>
        >>> # The ``FIRST_DEFAULT_ARG`` constant automatically selects the first default argument so it
        >>> # turns all default arguments into keyword-only ones. Both d0 and d1 are keyword-only arguments.
        >>> @first_kwonly_arg(FIRST_DEFAULT_ARG)
        >>> def func(a0, a1, d0='d0', d1='d1'):
        >>>     print(a0, a1, d0, d1)
        >>>
        >>> # ``@kwonly_defaults`` is a shortcut for the ``@first_kwonly_arg(FIRST_DEFAULT_ARG)``
        >>> # in the previous example. This example has the same effect as the previous one.
        >>> @kwonly_defaults
        >>> def func(a0, a1, d0='d0', d1='d1'):
        >>>     print(a0, a1, d0, d1)
    """
    def decorate(wrapped):
        if sys.version_info[0] == 2:
            arg_names, varargs, _, defaults = inspect.getargspec(wrapped)
        else:
            arg_names, varargs, _, defaults = inspect.getfullargspec(wrapped)[:4]

        if not defaults:
            raise TypeError("You can't use @first_kwonly_arg on a function that doesn't have default arguments!")
        first_default_index = len(arg_names) - len(defaults)

        if name is FIRST_DEFAULT_ARG:
            first_kwonly_index = first_default_index
        else:
            try:
                first_kwonly_index = arg_names.index(name)
            except ValueError:
                raise ValueError("%s() doesn't have an argument with the specified first_kwonly_arg=%r name" % (
                                 getattr(wrapped, '__name__', '?'), name))

        if first_kwonly_index < first_default_index:
            raise ValueError("The specified first_kwonly_arg=%r must have a default value!" % (name,))

        kwonly_defaults = defaults[-(len(arg_names)-first_kwonly_index):]
        kwonly_args = tuple(zip(arg_names[first_kwonly_index:], kwonly_defaults))
        required_kwonly_args = frozenset(arg for arg, default in kwonly_args if default is KWONLY_REQUIRED)

        def wrapper(*args, **kwargs):
            if required_kwonly_args:
                missing_kwonly_args = required_kwonly_args.difference(kwargs.keys())
                if missing_kwonly_args:
                    raise TypeError("%s() missing %s keyword-only argument(s): %s" % (
                                    getattr(wrapped, '__name__', '?'), len(missing_kwonly_args),
                                    ', '.join(sorted(missing_kwonly_args))))
            if len(args) > first_kwonly_index:
                if varargs is None:
                    raise TypeError("%s() takes exactly %s arguments (%s given)" % (
                                    getattr(wrapped, '__name__', '?'), first_kwonly_index, len(args)))
                kwonly_args_from_kwargs = tuple(kwargs.pop(arg, default) for arg, default in kwonly_args)
                args = args[:first_kwonly_index] + kwonly_args_from_kwargs + args[first_kwonly_index:]

            return wrapped(*args, **kwargs)

        return update_wrapper(wrapper, wrapped)
    return decorate


kwonly_defaults = first_kwonly_arg(FIRST_DEFAULT_ARG)


# -------------------------------------------------------------------------------------------------
# TESTS
# -------------------------------------------------------------------------------------------------


def get_arg_values(func, locals):
    args, varargs, varkw, _ = inspect.getargspec(func)
    if varargs:
        args.append(varargs)
    if varkw:
        args.append(varkw)
    return ' '.join('%s=%r' % (name, locals[name]) for name in args)


def test_functions():
    def run_one_test(func, first_kwonly_arg_name, *args, **kwargs):
        print('--------------------------------------------------------------------')
        print('          @first_kwonly_arg(%r)' % first_kwonly_arg_name)
        print('function: %s%s' % (func.__name__, inspect.formatargspec(*inspect.getargspec(func))))
        print('    args: %s' % (args,))
        print('  kwargs: %s' % (kwargs,))

        try:
            decorated = first_kwonly_arg(name=first_kwonly_arg_name)(func)
            decorated(*args, **kwargs)
        except Exception:
            import traceback
            traceback.print_exc()


    def run_all_tests_for_func(func):
        print('--------------------------------------------------------------------')
        print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        mode = func.__name__.split('_')[1]
        if 'a' in mode:
            # func has required args
            run_one_test(func, 'd1', 0, a1='my_a1')
            run_one_test(func, 'd1', 0, a1='my_a1', d0='my_d0')
            run_one_test(func, 'd1', 0, a1='my_a1', d2='my_d2')
            run_one_test(func, 'd1', 0, a1='my_a1', d0='my_d0', d2='my_d2')
            run_one_test(func, 'd1', a0='my_a0', a1='my_a1')
        else:
            run_one_test(func, 'd0')
            run_one_test(func, 'd1')
        run_one_test(func, 'd1', 0)
        run_one_test(func, 'd1', 0, 1)
        run_one_test(func, 'd1', 0, 1, 2)
        if 'v' in mode:
            # func has varargs
            run_one_test(func, 'd1', 0, 1, 2, 3)
            run_one_test(func, 'd1', 0, 1, 2, 3, 4)
            run_one_test(func, 'd1', 0, 1, 2, 3, 4, d2='my_d2')
            run_one_test(func, 'd1', 0, 1, 2, 3, 4, d1='my_d1', d2='my_d2')


    def run_all_tests_for_func_a(func):
        run_all_tests_for_func(func)



    def print_arg_values(func, locals):
        print('  result: ' + get_arg_values(func, locals))


    def func_r1(d0='d0', d1=KWONLY_REQUIRED, d2='d2'):
        print_arg_values(func_r1, locals())

    def func_r12(d0='d0', d1=KWONLY_REQUIRED, d2=KWONLY_REQUIRED):
        print_arg_values(func_r12, locals())

    def func_ad(a0, a1, d0='d0', d1='d1', d2='d2'):
        print_arg_values(func_ad, locals())

    def func_d(d0='d0', d1='d1', d2='d2'):
        print_arg_values(func_d, locals())

    def func_adv(a0, a1, d0='d0', d1='d1', d2='d2', *args):
        print_arg_values(func_adv, locals())

    def func_dv(d0='d0', d1='d1', d2='d2', *args):
        print_arg_values(func_dv, locals())

    run_one_test(func_ad, 'invalid_arg_name')
    run_one_test(func_ad, 'a0')
    run_one_test(func_ad, 'd0')
    run_one_test(func_ad, 'd1', 0, 1, 2, 3)
    run_one_test(func_ad, 'd1', 0, 1, 2, d0='my_d0')
    run_one_test(func_r1, 'd1')
    run_one_test(func_r12, 'd1')
    run_one_test(func_r1, 'd1', d2='my_d2')
    run_one_test(func_r1, 'd1', d1='my_d1')
    run_one_test(func_r12, 'd1', d1='my_d1')
    run_one_test(func_r12, 'd1', d1='my_d1', d2='my_d2')
    run_all_tests_for_func(func_ad)
    run_all_tests_for_func(func_d)
    run_all_tests_for_func(func_adv)
    run_all_tests_for_func(func_dv)


def test_class_methods():
    def instance_method(self, a0, a1, d0='d0', d1='d1', d2='d2', *args):
        print('instance_method: ' + get_arg_values(instance_method, locals()))

    def class_method(cls, a0, a1, d0='d0', d1='d1', d2='d2', *args):
        print('class_method: ' + get_arg_values(class_method, locals()))

    def static_method(a0, a1, d0='d0', d1='d1', d2='d2', *args):
        print('static_method: ' + get_arg_values(static_method, locals()))

    wrapped_instance_method = first_kwonly_arg('d1')(instance_method)
    wrapped_class_method = first_kwonly_arg('d1')(class_method)
    wrapped_static_method = first_kwonly_arg('d1')(static_method)

    class MyClass(object):
        instance_method = wrapped_instance_method
        class_method = classmethod(wrapped_class_method)
        static_method = staticmethod(wrapped_static_method)
    
        def __repr__(self):
            return MyClass.__name__ + '()'

    my_class_instance = MyClass()


    def run_one_test(method, *args, **kwargs):
        print('--------------------------------------------------------------------')
        print('method=%s args=%s, kwargs=%s' % (method.__name__, args, kwargs))
        try:
            method(*args, **kwargs)
        except Exception:
            import traceback
            traceback.print_exc()

    
    print('--------------------------------------------------------------------')
    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
    run_one_test(my_class_instance.instance_method, 0, 1)
    run_one_test(my_class_instance.instance_method, 0, 1, 2)
    run_one_test(my_class_instance.instance_method, 0, 1, 2, 3)
    run_one_test(my_class_instance.instance_method, 0, 1, 2, 3, d2='my_d2')
    run_one_test(my_class_instance.class_method, 0, 1)
    run_one_test(my_class_instance.class_method, 0, 1, 2)
    run_one_test(my_class_instance.class_method, 0, 1, 2, 3)
    run_one_test(my_class_instance.class_method, 0, 1, 2, 3, d2='my_d2')
    run_one_test(my_class_instance.static_method, 0, 1)
    run_one_test(my_class_instance.static_method, 0, 1, 2)
    run_one_test(my_class_instance.static_method, 0, 1, 2, 3)
    run_one_test(my_class_instance.static_method, 0, 1, 2, 3, d2='my_d2')


if __name__ == '__main__':
    test_functions()
    test_class_methods()
