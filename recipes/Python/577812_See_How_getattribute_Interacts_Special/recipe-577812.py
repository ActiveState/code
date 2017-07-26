# list of special methods from http://docs.python.org/py3k/reference/datamodel.html
names = {
        "control": "{}.control", # a normal method, for comparison

        "__new__": None,
        #"__new__": "{}()", # if an instance of type
        "__init__": None,
        #"__init__": "{}()", # if an instance of type
        "__prepare__": None,
        #"__prepare__": "{}()", # if an instance of type
        "__del__": "del {}",
        "__repr__": "repr({})",
        "__str__": "str({})",
        "__format__": "'{{}}'.format({})",
        "__lt__": "{} < 5",
        "__le__": "{} <= 5",
        "__eq__": "{} == 5",
        "__ne__": "{} != 5",
        "__gt__": "{} > 5",
        "__ge__": "{} >= 5",
        "__hash__": "hash({})",
        "__bool__": "bool({})",
        "__getattr__": None,
        #"__getattr__": "{}.x",
        "__getattribute__": None,
        #"__getattribute__": "{}.x",
        "__setattr__": "{}.x = 5",
        "__delattr__": "del {}.x",
        "__dir__": "dir({})",
        "__get__": None,
        "__set__": None,
        "__delete__": None,
        "__slots__": None,
        "__call__": "{}()",
        "__len__": "len({})",
        "__getitem__": "{}[1]",
        "__setitem__": "{}[1] = 5",
        "__delitem__": "del {}[1]",
        "__iter__": "iter({})",
        "__reversed__": "reversed({})",
        "__contains__": "5 in {}",
        "__add__": "{} + 5",
        "__sub__": "{} - 5",
        "__mul__": "{} * 5",
        "__truediv__": "{} / 5",
        "__floordiv__": "{} // 5",
        "__mod__": "{} % 5",
        "__divmod__": "divmod({}, 5)",
        "__pow__": "{}**5",
        "__lshift__": "{} << 5",
        "__rshift__": "{} >> 5",
        "__and__": "{} & 5",
        "__xor__": "{} ^ 5",
        "__or__": "{} | 5",
        "__radd__": "5 + {}",
        "__rsub__": "5 - {}",
        "__rmul__": "5 * {}",
        "__rtruediv__": "5 / {}",
        "__rfloordiv__": "5 // {}",
        "__rmod__": "5 % {}",
        "__rdivmod__": "divmod(5, {})",
        "__rpow__": "5 ** {}",
        "__rlshift__": "5 << {}",
        "__rrshift__": "5 >> {}",
        "__rand__": "5 & {}",
        "__rxor__": "5 ^ {}",
        "__ror__": "5 | {}",
        "__iadd__": "{} += 5",
        "__isub__": "{} -= 5",
        "__imul__": "{} *= 5",
        "__itruediv__": "{} /= 5",
        "__ifloordiv__": "{} //= 5",
        "__imod__": "{} %= 5",
        "__ipow__": "{} **= 5",
        "__ilshift__": "{} <<= 5",
        "__irshift__": "{} >>= 5",
        "__iand__": "{} &= 5",
        "__ixor__": "{} ^= 5",
        "__ior__": "{} |= 5",
        "__neg__": "-{}",
        "__pos__": "+{}",
        "__abs__": "abs({})",
        "__invert__": "~{}",
        "__complex__": "complex({})",
        "__int__": "int({})",
        "__float__": "float({})",
        "__round__": "round({})",
        "__index__": "oct({})",
        "__enter__": None,
        "__exit__": None,
        }

SOURCE = """\
def {0}(self, *args, **kwargs):
    raise Called
Test{0} = type("Test{0}", (Test,), dict({0}={0}))
test{0} = Test{0}()
{1}
"""

class InstanceChecked(Exception): pass
class Called(Exception): pass

class Test:
    def __getattribute__(self, name):
        raise InstanceChecked

skipped = []
for name in names:
    if not names[name]:
        skipped.append(name)
        continue

    print("#########################")
    print("  "+name)

    source = SOURCE.format(name, names[name].format("test"+name))
    try:
        exec(source, globals(), globals())
    except Called:
        print("   Doing it")
    except InstanceChecked:
        print("   --- instance __getattribute__ called")
    #except Exception:
    #    pass

print("#########################")
print("skipped {}: {}".format(len(skipped), skipped))
