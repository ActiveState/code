#!/usr/bin/env python


def enum(*names):
    """A true immutable symbolic enumeration with qualified value access."""

    class EnumValue(object):

        __slots__ = ("type", "value",)

        def __init__(self, type, value):
            self.type = type
            self.value = value

        def __hash__(self):
            return hash(self.value)

        def __cmp__(self, other):
            return cmp(self.value, other.value)

        def __invert__(self):
            return self.type.values[(len(self.type) - 1) - self.value]

        def __nonzero__(self):
            return bool(self.value)

        def __repr__(self):
            return str(self.type.names[self.value])

    class EnumClass(object):

        __slots__ = ("names", "mapping", "values",)

        def __init__(self, *names):
            self.names = names
            self.values = dict(
                (i, EnumValue(self, i)) for i in range(len(names))
            )
            self.mapping = dict(
                (names[i], value) for i, value in self.values.items()
            )

        def __getattr__(self, attr):
            try:
                return self.mapping[attr]
            except KeyError:
                raise AttributeError(attr)

        def __iter__(self):
            return iter(self.values.values())

        def __len__(self):
            return len(self.values)

        def __getitem__(self, i):
            return self.values[i]

        def __repr__(self):
            return "<Enum {0:s}>".format(str(self.names))

        def __str__(self):
            return "enum {0:s}".format(str(self.values))

    return EnumClass(*names)


Days = enum("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
print Days
print Days.Mon
print Days.Fri
print Days.Mon < Days.Fri
print list(Days)
for day in Days:
    print "Day: {0:s}".format(repr(day))

Confirmation = enum("No", "Yes")
answer = Confirmation.No
print "Your answer is not", ~answer
