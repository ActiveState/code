class EnumItem(int):
    
    __slots__ = ['name']

    def __new__(cls, name, value):
        i = int.__new__(cls, value)
        i.name = name
        return i

    def getname(self):
        return self.name


def enum(func):
    names = func.func_code.co_varnames
    defaults = func.func_defaults
    if defaults is None:
        defaults = []
    n = len(names)-len(defaults)
    values = range(n)+list(defaults)
    for i, name in zip(values, names):
        item = EnumItem(name, i)
        setattr(func, name, item)
    return func




# ________________________________________________
# tests

def test_enum():
    @enum
    def colors(red, green, blue):
        pass
    assert colors.red == 0
    assert colors.green == 1
    assert colors.blue == 2


def test_getname():
    @enum
    def colors(red, green, blue):
        pass
    assert colors.red.getname() == 'red'
    assert colors.green.getname() == 'green'
    assert colors.blue.getname() == 'blue'

def test_default_value():
    @enum
    def colors(red, green, blue=42):
        pass
    assert colors.red == 0
    assert colors.green == 1
    assert colors.blue == 42
