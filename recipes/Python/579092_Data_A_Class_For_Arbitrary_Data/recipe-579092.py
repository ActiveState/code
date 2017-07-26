'module data provides class Data(object)'

from pprint import pformat

class Data(object):
    "represents arbitrary data; provides functionality for displaying itself"\
    " properly"

    def __init__(self, *args, **kwargs):
        if args:
            self.args = args
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.assert_data()

    def __repr__(self):
        if 'args' in self.__dict__:
            args = map(repr, self.args)
        else:
            args = []
        for key, value in self.__dict__.items():
            if key != 'args':
                args.append('%s=%r' % (key, value))
        return self.__class__.__name__ + '(' + (', '.join(args)) + ')'

    def __str__(self):
        return self.formatted()

    def assert_data(self):
        "to be overridden for internal asserts after creation"

    def stringify_arg(key, value, indent=None, variables=None):
        if indent is None:
            indent = '  '
        if isinstance(value, Data):
            if variables is None:
                variables = {}
            keys, values = variables.keys(), variables.values()
            try:
                i = values.index(value)
            except ValueError:
                return ('%s%s = %s' %
                        (indent, key,
                         value.formatted(indent=indent).
                         replace('\n', '\n%s%*s' % (indent, len(key)+3, ''))))
            else:
                return ('%s%s = %s' %
                        (indent, key, keys[i]))
        else:
            return ('%s%s = %s' %
                    (indent, key,
                     pformat(value).replace('\n',
                                            '\n%s%*s' %
                                            (indent, len(key)+3, ''))))

    stringify_arg = staticmethod(stringify_arg)

    def formatted(self, indent=None, variables=None):
        result = [ self.__class__.__name__ + ':' ]
        if 'args' in self.__dict__:
            result.append(Data.stringify_arg('args', self.args,
                                             indent=indent,
                                             variables=variables))
        for key, value in self.__dict__.items():
            if key != 'args':
                result.append(Data.stringify_arg(key, value,
                                                 indent=indent,
                                                 variables=variables))
        return '\n'.join(result)
