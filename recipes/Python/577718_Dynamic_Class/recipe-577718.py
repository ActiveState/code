from collections import namedtuple


Param = namedtuple("Param", "name default doc")
ReqParam = namedtuple("ReqParam", "name doc")
Getter = namedtuple("Getter", "name initial doc")


PROPERTY_TEMPLATE = """\
@property
def {name}(self):
    "{doc}"
    if not hasattr(self, "_{name}"):
        self._{name} = {initial}
    return self._{name}"""


def dataclass(typename, doc, params, properties, verbose=False):
    "Return a new class around the params and properties."

    namespace = {}

    # handle class docstring
    if not doc:
        doc = ""
    docstring = doc.splitlines()
    if not docstring:
        docstring = ['""']
    elif len(docstring) > 1:
        docstring.insert(0, '"""')
        docstring.append('"""')
        docstring.extend(line for line in doc.splitlines)
    else:
        docstring = ['"{}"'.format(docstring[0])]

    # handle __init__ and params
    params_constant = []
    __init__ = []
    if params:
        params_constant = ["PARAMS = ("]
        doc = []
        assignment = []
        for param in params:
            params_constant.append("        {}{},".format(
                    param.__class__.__name__,
                    param.__getnewargs__(),
                    ))
            namespace[param.__class__.__name__] = param.__class__
            default = ""
            if hasattr(param, "default"):
                default = param.default
                if hasattr(default, "__name__"):
                    namespace[default.__name__] = default
                    default = default.__name__
                default = "={}".format(default)
            __init__.append("    {}{},".format(param.name, default))
            if param.doc:
                doc.append("  {} - {}".format(param.name, param.doc))
            assignment.append("self.{} = {}".format(param.name, param.name))
        __init__.append("):")
        params_constant.append("        )")
        if doc:
            __init__.append('"""')
            __init__.append("Parameters:")
            __init__.extend(doc)
            __init__.append("")
            __init__.append('"""')
            __init__.append("")
        __init__.extend(assignment)

        __init__ = ["    "+line for line in __init__]
        __init__.insert(0, "def __init__(self,")

    # handle properties
    properties_constant = []
    props = []
    for prop in properties:
        properties_constant.append("        {}{},".format(
                prop.__class__.__name__,
                prop.__getnewargs__(),
                ))
        namespace[prop.__class__.__name__] = prop.__class__
        initial = prop.initial
        if hasattr(initial, "__name__"):
            namespace[initial.__name__] = initial
            initial = initial.__name__
        prop = PROPERTY_TEMPLATE.format(
                name=prop.name,
                initial=initial,
                doc=prop.doc,
                )
        props.extend(prop.splitlines())
        props.append("")
    if properties_constant:
        properties_constant.insert(0, "PROPERTIES = (")
        properties_constant.append("        )")

    # put it all together
    template = ["class {}(object):".format(typename)]
    template.extend("    "+line for line in docstring)
    template.extend("    "+line for line in params_constant)
    template.extend("    "+line for line in properties_constant)
    template.append("")
    template.extend("    "+line for line in __init__)
    template.append("")
    template.extend("    "+line for line in props)
    template.append("")
    template = "\n".join(template)

    if verbose:
        print(template)
    try:
        exec(template, namespace)
    #except SyntaxError, e:
    except SyntaxError as e:
        raise SyntaxError(e.msg + ':\n' + template)
    return namespace[typename]


def data(cls):
    "A class decorator for the dataclass function."
    return dataclass(cls.__name__, cls.__doc__, cls.PARAMS, cls.PROPERTIES)
