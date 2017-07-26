# Auto-prints a string using the new (as of 2.4) string-template
# based substitution.
import copy, inspect
from string import Template

def printfmt(template):
    frame = inspect.stack()[1][0]
    try:
        var = copy.copy(frame.f_globals)
        var.update(frame.f_locals)
        print Template(template).safe_substitute(var)
    finally:
        del frame
