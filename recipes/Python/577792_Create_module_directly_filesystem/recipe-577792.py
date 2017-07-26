import runpy
import imp

def mod_from_file(mod_name, path):
    """Runs the Python code at path, returns a new module with the resulting globals"""
    attrs = runpy.run_path(path, run_name=mod_name)
    mod = imp.new_module(mod_name)
    mod.__dict__.update(attrs)
    return mod

# Example usage

>>> import timeit
>>> timeit2 = mod_from_file("timeit2", timeit.__file__)
>>> dir(timeit2)
['Timer', '__all__', '__builtins__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '_template_func', 'default_number', 'default_repeat', 'default_timer', 'dummy_src_name', 'gc', 'itertools', 'main', 'reindent', 'repeat', 'sys', 'template', 'time', 'timeit']
