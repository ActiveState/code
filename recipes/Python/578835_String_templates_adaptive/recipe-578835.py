import string
import sys

class IndentFormatter(string.Formatter):
    def parse(self,format_string):
        parsed = string.Formatter.parse(self,format_string)
        for (literal_text, field_name, format_spec, conversion) in parsed:
            last_newline = literal_text.rfind('\n')
            indentation = literal_text[last_newline+1:]
            if indentation.isspace():
                format_spec = '|{0}|{1}'.format(len(indentation),format_spec)
            yield literal_text, field_name, format_spec, conversion
    def format_field(self,value,format_spec):
        if format_spec.startswith('|'):
            nspaces,_,old_format_spec = format_spec[1:].partition('|')
            return trim(string.Formatter.format_field(self,value,old_format_spec),int(nspaces))
        else:
            return string.Formatter.format_field(self,value,format_spec)
        
# from PEP 257, extended with addindent
def trim(docstring,addindent=0):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return ('\n'+' '*addindent).join(trimmed)        

class C(str):
    def format(self,*args,**kwargs):
        return C(IndentFormatter().format(self,*args,**kwargs))

def test():
    arrayvars = ['arr{n}'.format(n=n) for n in range(3)]
    array_length = 1000;
    array_args = ', '.join('int* {var}'.format(var=var) for var in arrayvars)
    array_product = ' * '.join('{var}[i]'.format(var=var) for var in arrayvars)
    freearrays = '\n'.join('free({var});'.format(var=var) for var in arrayvars)
    body = C('''
             candidate = {array_product};
             if (candidate>max)
                max = candidate;
             ''').format(**locals())
    fun = C('''
            int max_product({array_args}) {{
                int max = 0;
                int candidate;
                int i;
                for (i=0; i<{array_length}; i++) {{
                    {body}
                }}
                {freearrays}
                return max;
            }}
            ''').format(**locals())
    print(fun)
