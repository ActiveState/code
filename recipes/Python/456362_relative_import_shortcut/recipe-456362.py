import os
import sys

def pythonImport(name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    base_name = os.path.basename(current_path).split('.')[0]
    sys.path[:] = [path for path in sys.path
                   if os.path.abspath(path) != os.path.abspath(current_path)]

    original_module = sys.modules[name]
    del sys.modules[name]
    python_module = __import__(name)
    python_module_name = 'python_%s' % name
    sys.modules[python_module_name] = python_module
    sys.path.append(current_path)
    sys.modules[name] = original_module
    return python_module_name, python_module
