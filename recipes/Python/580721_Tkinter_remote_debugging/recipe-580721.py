# Author: Miguel Martinez Lopez
#
# This code require rpyc.
# You can install rpyc typing:
#     pip install rpyc
#
# Run this code and in an another interactive interpreter write this:
# >>> import rpyc
# ... c = rpyc.classic.connect("localhost")
# >>> c.execute("from Tkinter import Label; label=Label(app, text='a label')")
# ... c.execute("label.pack()")
# >>> app = c.eval("app")
# >>> app.responsive_button.invoke()


from rpyc.utils.server import ThreadedServer
from rpyc.utils.classic import DEFAULT_SERVER_PORT
from rpyc.core.service import Service, ModuleNamespace

from rpyc.lib.compat import execute, is_py3k

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
        execute(text, PublicService.exposed_namespace)
    def exposed_eval(self, text):
        """evaluate arbitrary code (using ``eval``)"""
        return eval(text, PublicService.exposed_namespace)
    def exposed_getmodule(self, name):
        """imports an arbitrary module"""
        return __import__(name, None, None, "*")
    def exposed_getconn(self):
        """returns the local connection instance to the other side"""
        return self._conn


if __name__ == "__main__":
    import threading  


    from Tkinter import Tk, Button
    import tkMessageBox

    class App(Tk):
        def __init__(self):
            Tk.__init__(self)

            self.responsive_button = Button(self, text="It's responsive", command = lambda:tkMessageBox.showinfo("alert window", "It's responsive!"))
            self.responsive_button.pack()


    app = App()

    # Add here all the exposed objects in the shared namespace
    PublicService.exposed_namespace = {"app":app}

    t = threading.Thread(target=lambda: ThreadedServer(PublicService, hostname = "localhost", port=DEFAULT_SERVER_PORT).start())
    t.daemon=True
    t.start()
    app.mainloop()
