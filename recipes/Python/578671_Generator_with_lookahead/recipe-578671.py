import Queue
import threading

class BackgroundGenerator(threading.Thread):
    def __init__(self, generator, lookahead=10):
        threading.Thread.__init__(self)
        self.queue = Queue.Queue(lookahead)
        self.generator = generator
        self.daemon = True
        self.start()

    def __iter__(self):
        return self

    def run(self):
        for item in self.generator:
            self.queue.put(item)
        self.queue.put(None)

    def next(self):
            next_item = self.queue.get()
            if next_item is None:
                 raise StopIteration
            return next_item



def test():
    import time

    def processing_releasing_GIL(process_time):
        # simulating processing that releases the Global Interpreter Lock
        # also see: https://wiki.python.org/moin/GlobalInterpreterLock
        time.sleep(process_time)

    def processing_no_release_GIL(n):
        i = 0
        while i < n:
           i += 1

    def generator_count_up_release_GIL(count, process_time):
        x = 1
        while x <= count:
            yield x
            processing_releasing_GIL(process_time)
            x += 1

    def generator_count_up_not_releasing_GIL(count, n):
        x = 1
        while x <= count:
            yield x
            processing_no_release_GIL(n)
            x += 1

    print "Testing runtime of a generator that releases the GIL."
    n = 10
    # test runtime without backgroundGenerator
    start = time.time()
    gen1 = generator_count_up_release_GIL(n, 0.1)
    counter = 0
    for i in gen1:
        counter = i
        processing_releasing_GIL(0.1)
    print "- no BackgroundGenerator:  ", counter, time.time() - start

    # test runtime WITH backgroundGenerator
    start = time.time()
    gen2 = BackgroundGenerator(generator_count_up_release_GIL(n, 0.1))
    counter = 0
    for i in gen2:
        counter = i
        processing_releasing_GIL(0.1)
    print "- with BackgroundGenerator:", counter, time.time() - start


    print "Testing runtime of a generator that does not release the GIL."
    iterations = 2000000
    # test runtime without backgroundGenerator
    start = time.time()
    gen1 = generator_count_up_not_releasing_GIL(n, iterations)
    counter = 0
    for i in gen1:
        counter = i
        processing_no_release_GIL(iterations)
    print "- no BackgroundGenerator:  ", counter, time.time() - start

    # test runtime WITH backgroundGenerator
    start = time.time()
    gen2 = BackgroundGenerator(generator_count_up_not_releasing_GIL(n, iterations))
    counter = 0
    for i in gen2:
        counter = i
        processing_no_release_GIL(iterations)
    print "- with BackgroundGenerator:", counter, time.time() - start


if __name__=="__main__":
    test()
