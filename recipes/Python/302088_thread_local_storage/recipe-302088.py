import threading

class ThreadLocalExample:
    def __init__(self):
        self.local = threading.local()

    def run(self):
        import random, time
        self.local.foo = []
        for i in range(10):
            self.local.foo.append(random.choice(range(10)))
            print threading.currentThread(), self.local.foo
            # A small sleep to let the threads run in different orders
            time.sleep(random.random())


example = ThreadLocalExample()
for i in range(4):
    t = threading.Thread(target=example.run)
    t.start()
