def generate_dispatcher(method_handler, parent_class=None):
    """
    Create a dispatcher class and return an instance of it from a dispatcher
    definition.
    The definition is a class with the following attributes:
    _ EXPORTED_METHOD: dictionary where keys are method names and values
      class attribute names of the attributes holding references to an object
      implementing the method 
    _ attributes defined in EXPORTED_METHODS values. They must contain an
      object instance which implements the respective methods (EXPORTED_METHODS
      keys)

    Ex:
    class TestDispatchHandler:
        EXPORTED_METHODS = {'method1': 'attr1',
                            'method2': 'attr1',
                            'method3': 'attr2'}
        attr1 = Object1()
        attr2 = Object2()

    where Object1 is a class which provides method1 and method2 and Object2 a
    class which provides method3

    obj_inst = generate_dispatcher(TestDispatchHandler)

    will affect in 'obj_inst' a class instance which provide method1, method2
    and method3 by delegate it to the correct object
    """
    # class definition
    if parent_class:
        class_str = 'class Dispatcher(%s):\n' % parent_class
        statements = '  %s.__init__(self)\n' % parent_class
    else:
        class_str = 'class Dispatcher:\n'
        statements = ''

    # methods definition
    registered = []
    for method, objname in method_handler.EXPORTED_METHODS.items():
        if not objname in registered:
            registered.append(objname)
        class_str = '%s def %s(self, *attrs):\n  return self.%s.%s(*attrs)\n'%\
                    (class_str, method, objname, method)

    # constructor definition
    attrs = ''
    for objname in registered:
        attrs = '%s, %s' % (attrs, objname)
        statements = '%s  self.%s=%s\n' % (statements, objname, objname)
        # retrieve object reference in current context
        exec '%s=getattr(method_handler, "%s")'%(objname, objname)

    # assemble all parts
    class_str = '%s def __init__(self%s):\n%s' % (class_str, attrs, statements)

    # now we can eval the full class
    exec class_str

    # return an instance of constructed class
    return eval('Dispatcher(%s)'%attrs[2:]) # attrs[2:] for removing ', '
