def ObserverProxy(method_names):
    class Proxy:
        def __init__(self):
            self._observers = []
        def add_observer(self, observer):
            self._observers.append(observer)
        def remove_observer(self, observer):
            self._observers.remove(observer)

    def create_method_proxy(method_name):
        def method_proxy(self, *args, **kwargs):
            for observer in self._observers:
                getattr(observer, method_name)(*args, **kwargs)
        return method_proxy

    for method_name in method_names:
        setattr(Proxy, method_name, create_method_proxy(method_name))

    return Proxy()

if __name__ == "__main__":
    # usage example

    output_proxy = ObserverProxy(["write", "close"])

    import sys
    output_proxy.add_observer(sys.stdout)
    output_proxy.add_observer(sys.stderr)
    output_proxy.add_observer(file("somefile", "w"))

    print >>output_proxy, "This goes to all observers"
    output_proxy.close()
