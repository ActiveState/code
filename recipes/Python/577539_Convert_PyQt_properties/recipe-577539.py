def iterProperties(cls):
    """
    Iterates through the names of all the properties on a PyQt class.
    """
    meta = cls.staticMetaObject
    for i in range(meta.propertyCount()):
        yield meta.property(i).name()

def useProperties(cls):
    """
    Adds Python properties for each Qt property in a class.
    """
    def getter(name):
        def get(self):
            return self.property(name)
        return get
    def setter(name):
        def set(self, value):
            return self.setProperty(name, value)
        return set
    for name in iterProperties(cls):
        setattr(cls, name, property(getter(name), setter(name)))
    return cls

# use in Python 3
@useProperties
class Widget(QtGui.QWidget):
    pass

# or simply
useProperties(QtGui.QWidget)

# then
w = QtGui.QWidget()
w.font = QtGui.QFont('Droid Sans Mono')
