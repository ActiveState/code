def _is_pickleable(obj):
    "Is the object pickleable?"
    import cPickle as pickle
    try:
        pickle.dumps(obj)
        return True
    except TypeError:
        return False

class UnpickleableFieldError(Exception): pass

def add_fields_pickling(klass, disable_unpickleable_fields=False):
    """
    Add pickling for 'fields' classes.

    A 'fields' class is a class who's methods all act as fields - accept no
    arguments and for a given class's state always return the same value.

    Useful for 'fields' classes that contain unpickleable members.

    Used in TestOOB, http://testoob.sourceforge.net

    A contrived example for a 'fields' class:

      class Titles:
        def __init__(self, name):
          self.name = name
        def dr(self):
          return "Dr. " + self.name
        def mr(self):
          return "Mr. " + self.name

    If a method returns an unpickleable value there are two options:
    Default:
      Allow the instance to be pickled. If the method is called on the
      unpickled instance, an UnpickleableFieldError exception is raised.
      There is a possible performance concern here: each return value is
      pickled twice when pickling the instance.

    With disable_unpickleable_fields=True:
      Disallow pickling of instances with a method returning an unpickleable
      object.
    """
    def state_extractor(self):
        from types import MethodType

        fields_dict = {}
        unpickleable_fields = []

        def save_field(name, method):
            try:
                retval = method()
                if disable_unpickleable_fields or _is_pickleable(retval):
                    fields_dict[name] = retval # call the method
                else:
                    unpickleable_fields.append(name)
            except TypeError:
                raise TypeError("""not a "fields" class, problem with method '%s'""" % name)

        for attr_name in dir(self):
            if attr_name in ("__init__", "__getstate__", "__setstate__"):
                continue # skip constructor and state magic methods

            attr = getattr(self, attr_name)

            if type(attr) == MethodType:
                save_field(attr_name, attr)

        return (fields_dict, unpickleable_fields)

    def build_from_state(self, state):
        fields_dict, unpickleable_fields = state
        # saved fields
        for name in fields_dict.keys():
            # set the default name argument to prevent overwriting the name
            setattr(self, name, lambda name=name:fields_dict[name])

        # unpickleable fields
        for name in unpickleable_fields:
            def getter(name=name):
                raise UnpickleableFieldError(
                        "%s()'s result wasn't pickleable" % name)
            setattr(self, name, getter)

    klass.__getstate__ = state_extractor
    klass.__setstate__ = build_from_state

#
# Example
#

class FileInfo:
    "Unpickleable because of a file field"
    def __init__(self, filename):
        self.file = file(filename)

    def get_fileno(self):
        return self.file.fileno()

    def get_num_lines(self):
        self.file.seek(0)
        return len(self.file.readlines())

    def get_name(self):
        return self.file.name

    def get_file(self):
        return self.file


import pickle
finfo = FileInfo("some_file")

try:
    # This won't work, can't pickle a file object
    pickled_string = pickle.dumps(finfo)
except TypeError:
    print "Pickle failed"

# Registering the new pickler
add_fields_pickling(FileInfo)

finfo = FileInfo("some_file")

pickled_string = pickle.dumps(finfo) # Succeeds
print "Pickle succeeded"

finfo2 = pickle.loads(pickled_string)

print "name:     ", finfo2.get_name()
print "fileno:   ", finfo2.get_fileno()
print "num_lines:", finfo2.get_num_lines()
print "file:     ",
try:
    print finfo2.get_file()
except UnpickleableFieldError, e:
    print e

# This will print:
#
# name:      some_file
# fileno:    3
# num_lines: 218
# file:      get_file()'s result wasn't pickleable
