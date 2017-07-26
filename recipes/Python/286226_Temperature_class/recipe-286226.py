class Temperature(object):
    equations = {'c': (1.0, 0.0, -273.15), 'f': (1.8, -273.15, 32.0),
                 'r': (1.8, 0.0, 0.0)}

    def __init__(self, k=0.0, **kwargs):
        self.k = k
        for k in kwargs:
            if k in ('c', 'f', 'r'):
                setattr(self, k, kwargs[k])
                break

    def __getattr__(self, name):
        if name in self.equations:
            eq = self.equations[name]
            return (self.k + eq[1]) * eq[0] + eq[2]
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in self.equations:
            eq = self.equations[name]
            self.k = (value - eq[2]) / eq[0] - eq[1]
        else:
            object.__setattr__(self, name, value)

    def __str__(self):
        return "%g K" % self.k

    def __repr__(self):
        return "Temperature(%g)" % self.k
