import formencode
from formencode import validators

def validate(schema):
    def fn(realfn):
        def wrapper(*args, **kws):
            field_names = schema.fields.keys()
            args_dict = dict(zip(realfn.func_code.co_varnames, args))
            args_dict.update(dict((field_name, kws.get(field_name)) for field_name in field_names if field_name in kws))
            schema().to_python(args_dict)
            return realfn(*args, **kws)
        return wrapper
    return fn


class GreetSchema(formencode.Schema):
    name = validators.String(not_empty=True)


@validate(GreetSchema)
def greet(name):
    print 'hello', name

greet('shon')
greet(name='shon')
greet('')
