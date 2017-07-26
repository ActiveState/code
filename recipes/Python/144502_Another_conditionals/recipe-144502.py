def If(cond, truepart, falsepart):
    import inspect

    # Get the global namespace.
    globalns = globals()

    # Get the caller namespace
    localns = inspect.currentframe(1).f_locals

    # Evaluate according to 'cond'
    if cond:
        return eval(truepart, globalns, localns)
    else:
        return eval(falsepart, globalns, localns)


# Example of use
def spam(x):
    print If(x==0, '"Is zero"', '1.0/x')

spam(4)    # prints 0.25
spam(0)    # prints "Is zero"
