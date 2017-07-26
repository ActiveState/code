# -*- coding: utf-8 -*-


class alias(object):
    """
    Alias class that can be used as a decorator for making methods callable
    through other names (or "aliases").
    Note: This decorator must be used inside an @aliased -decorated class.
    For example, if you want to make the method shout() be also callable as
    yell() and scream(), you can use alias like this:

        @alias('yell', 'scream')
        def shout(message):
            # ....
    """

    def __init__(self, *aliases):
        """Constructor."""
        self.aliases = set(aliases)

    def __call__(self, f):
        """
        Method call wrapper. As this decorator has arguments, this method will
        only be called once as a part of the decoration process, receiving only
        one argument: the decorated function ('f'). As a result of this kind of
        decorator, this method must return the callable that will wrap the
        decorated function.
        """
        f._aliases = self.aliases
        return f


def aliased(aliased_class):
    """
    Decorator function that *must* be used in combination with @alias
    decorator. This class will make the magic happen!
    @aliased classes will have their aliased method (via @alias) actually
    aliased.
    This method simply iterates over the member attributes of 'aliased_class'
    seeking for those which have an '_aliases' attribute and then defines new
    members in the class using those aliases as mere pointer functions to the
    original ones.

    Usage:
        @aliased
        class MyClass(object):
            @alias('coolMethod', 'myKinkyMethod')
            def boring_method():
                # ...

        i = MyClass()
        i.coolMethod() # equivalent to i.myKinkyMethod() and i.boring_method()
    """
    original_methods = aliased_class.__dict__.copy()
    for name, method in original_methods.iteritems():
        if hasattr(method, '_aliases'):
            # Add the aliases for 'method', but don't override any
            # previously-defined attribute of 'aliased_class'
            for alias in method._aliases - set(original_methods):
                setattr(aliased_class, alias, method)
    return aliased_class


#
# A very simple example
#

@aliased
class Vehicle(object):
    def __init__(self, brand, model, color):
        """Constructor."""
        self.brand = brand
        self.model = model
        self.color = color

    @alias('modelBrandAndColor', 'getModelBrandAndColour', 'getDescription')
    def model_brand_and_color(self):
        """Get the model and brand of this Vehicle."""
        return '{0} {1} {2}'.format(self.color, self.brand, self.model)

vehicle = Vehicle('Chevrolet', 'Spark', 'black')
# Now your API looks like your users would want.
# Any of the following lines is equivalent to the others:
print vehicle.model_brand_and_color()
print vehicle.getDescription()
print vehicle.modelBrandAndColor()
print vehicle.getModelBrandAndColour()
