# Author: Miguel Martinez Lopez

from rpyc.utils.server import ThreadedServer
from rpyc.utils.classic import DEFAULT_SERVER_PORT
from rpyc.core.service import Service, ModuleNamespace

from rpyc.lib.compat import execute, is_py3k

import sys
import os
import threading
import argparse
    
EXECUTED_PYTHON_FILE = False

def exec_python(filepath, namespace):
    global EXECUTED_PYTHON_FILE

    if EXECUTED_PYTHON_FILE:
        raise Exception("exec_python can be used only one time")

    EXECUTED_PYTHON_FILE = True

    filepath = os.path.abspath(filepath)
    sys.path = [os.path.dirname(filepath)] + sys.path[1:]

    namespace["__file__"] = filepath
    namespace["__name__"] = "__main__"

    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), namespace)


class PublicService(Service):
    exposed_namespace = {}

    def on_connect(self):
        self._conn._config.update(dict(
            allow_all_attrs = True,
            allow_pickle = True,
            allow_getattr = True,
            allow_setattr = True,
            allow_delattr = True,
            import_custom_exceptions = True,
            instantiate_custom_exceptions = True,
            instantiate_oldstyle_exceptions = True,
        ))

        # shortcuts
        self._conn.modules = ModuleNamespace(self._conn.root.getmodule)
        self._conn.eval = self._conn.root.eval
        self._conn.execute = self._conn.root.execute
        self._conn.namespace = self._conn.root.namespace
        if is_py3k:
            self._conn.builtin = self._conn.modules.builtins
        else:
            self._conn.builtin = self._conn.modules.__builtin__
        self._conn.builtins = self._conn.builtin

    def exposed_execute(self, text):
        """execute arbitrary code (using ``exec``)"""
        execute(text, self.exposed_namespace)
    def exposed_eval(self, text):
        """evaluate arbitrary code (using ``eval``)"""
        return eval(text, self.exposed_namespace)
    def exposed_getmodule(self, name):
        """imports an arbitrary module"""
        return __import__(name, None, None, "*")
    def exposed_getconn(self):
        """returns the local connection instance to the other side"""
        return self._conn

parser = argparse.ArgumentParser(description='Remote debugging and testing')
parser.add_argument('filename', help="Path to script")
parser.add_argument('-p', '--port', action="store", dest="port", default=DEFAULT_SERVER_PORT, help="Remote interpreter port", type=int)

args = parser.parse_args()
thread = threading.Thread(target=lambda: ThreadedServer(PublicService, hostname = "localhost", port=args.port).start())
thread.daemon=True
thread.start()

exec_python(args.filename, PublicService.exposed_namespace)
