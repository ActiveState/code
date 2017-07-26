import time, threading, Queue

class throttle:
    def __init__(self, func, cps, daemon = 0, resolution = 0.1):
        self.func = func
        self.cps = cps
        self.res = resolution
        self.queue = Queue.Queue()
        self.thr = threading.Thread(target = self._loop)
        self.thr.setDaemon(daemon)
        self.thr.start()

    def destroy(self):
        if self.thr.isAlive():
            self.queue.put(self.queue) # kills the thread
            if not self.thr.isDaemon():
                self.thr.join()

    def __call__(self, data):
        self.queue.put(data)

    def _loop(self):
        while 1:
            data = self.queue.get()
            if data == self.queue:
                return # the queue instance serves as a trigger object
            t = time.time()
            self.func(data)
            while len(data) / (time.time() - t + 0.0001) > self.cps:
                time.sleep(self.res)


if __name__ == '__main__':
    import sys
    
    p = throttle(sys.stdout.write, 30)

    p("HEAD KNIGHT: We are now... no longer the Knights Who Say 'Ni'.\n")
    p("KNIGHTS OF NI: Ni! Shh!\n")
    p("HEAD KNIGHT: Shh! We are now the Knights Who Say "
      "'Ecky-ecky-ecky-ecky-pikang-zoop-boing-goodem-zu-owly-zhiv'.\n")
    p("RANDOM: Ni!\n")

    p.destroy()
