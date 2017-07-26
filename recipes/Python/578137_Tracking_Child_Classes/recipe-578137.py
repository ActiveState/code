class ChildTracker(type):
  def __new__(cls, name, bases, dict_):
    new_class = type.__new__(cls, name, bases, dict_)
    # Check if this is the tracking class
    if '__metaclass__' in dict_ and dict_['__metaclass__']==ChildTracker:
      new_class.child_classes = {}
    else:
      # Add the new class to the set
      new_class.child_classes[name] = new_class
    return new_class


class BaseClass(object):
  __metaclass__ = ChildTracker


class Child1(BaseClass):
  pass

class Child2(BaseClass):
  pass

print BaseClass.child_classes.keys()
