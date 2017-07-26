"""
Name-Value Object: $obj.attr.attr2|filter|filter2|filterN
Numbered Argument: $[0].attr.attr2|filter|filter2|filterN

To create new filters, subclass and create do_ method.
do_ALL is the general method for any filters not found. It should raise FilterError if the
filter is still not available.

Use $$ to avoid replacement
"""

import re
from string import capwords

class FilterError(Exception): pass

r_macro = re.compile(r"""
                    \$                                                  # must start with $, not $$
                    (                                                   # start group
                    \[\d+\][.|][a-zA-Z0-9]+[a-zA-Z0-9|.]*               # opening [number] + attrs / filters
                    |                                                   # 2nd case
                    \[\d+\]                                             # opening [number] + filters
                    |                                                   # 3rd case
                    [a-zA-Z][a-zA-Z0-9]+[.|][a-zA-Z0-9]+[a-zA-Z0-9|.]*  # obj + attrs / filters
                    |                                                   # 4th case
                    [a-zA-Z][a-zA-Z0-9]+                                # obj + attrs / filters
                    )                                                   # done
                    """, re.VERBOSE)

class Template:

    def __init__(self, string=''):
        self.buffer = string
        self.filterregister = {'length': len}

    def load(self, string):
        self.buffer += string

    def register_filter(self, name, func):
        self.filterregister[name] = func

    def remove_filter(self, name):
        func = self.filterregister[name]
        del self.filterregister[name]
        return func

    def do_capwords(self, string):
        return capwords(string)

    def do_capfirst(self, string):
        return string[0].capitalize() + string[1:]

    def do_ALL(self, string, filter_name):
        """General filter for all filter types not found"""
        if hasattr(str, filter_name):
            return getattr(str, filter_name)(string)
        else:
            raise FilterError('No such filter as %r'%filter_name)

    def render(self, *args, **kwargs):
        """Render the template, replacing macros along the way"""
        bufferstring = str(self.buffer)
        for matchedstring in r_macro.findall(self.buffer):
            # this list should contain the name of the object first, then the attrs needed
            obj_and_attrs = matchedstring.split('.')
            # remove the filters from the attr string
            obj_and_attrs[-1] = obj_and_attrs[-1].split('|', 1)[0]
            obj, attrs = obj_and_attrs[0], obj_and_attrs[1:]

            if obj.startswith('['):
                index = int(obj[1:-1])
                if not index < len(args):
                    #raise ValueError("No object at index %s!"%index)
                    bufferstring = bufferstring.replace('$'+matchedstring, '')
                    continue
                else:
                    obj = args[index]
            
            else:
                if obj not in kwargs:
                    #raise ValueError("No object with name %r"%obj)
                    bufferstring = bufferstring.replace('$'+matchedstring, '')
                    continue
                obj = kwargs[obj]

            value = obj
            if len(attrs) > 0:
                for attr in attrs:
                    if not attr:
                        raise ValueError("Cannot have empty attr!")
                    try:
                        value = getattr(value, attr)
                    except AttributeError:
                        value = value[attr]

            filters = matchedstring.split('|')[1:]

            for filtername in filters:
                if not filtername:
                    raise ValueError("Cannot have empty filter!")
                try:
                    value = getattr(self, "do_"+filtername)(value)
                except AttributeError:
                    try:
                        value = self.filterregister[filtername](value)
                    except KeyError:
                        value = self.do_ALL(value, filtername)

            bufferstring = bufferstring.replace('$'+matchedstring, str(value))
                    
        return bufferstring.replace('$$', '$').replace('\.', '.')


def render_from_string(templatestring, *args, **kwargs):
    """Shortcut function"""
    t = Template(templatestring)
    return t.render(*args, **kwargs)
    
if __name__ == "__main__":
    tempstr = """Hello $fullname|capwords,
I am writing to inform you that your child, $firstname|capitalize $lastname|capitalize has recieved
a grade of $grade% in this $coursename course. I strongly believe that your child has much potential
and could do much better if he/she tried.

I require $$100.00 for the field trip next week. We will be going to $[0] on $[1]\."""

    print render_from_string(tempstr, "Edworthy Park", "Tuesday", fullname="Bob joe", firstname="James", lastname="Clark maxwell", grade=75, coursename="Astronomy")
