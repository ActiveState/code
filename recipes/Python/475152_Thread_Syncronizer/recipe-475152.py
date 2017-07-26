import thread

class sync:

    def __init__(self, threads):
        self.__threads = threads
        self.__count = 0
        self.__main = thread.allocate_lock()
        self.__exit = thread.allocate_lock()
        self.__exit.acquire()

    def sync(self):
        self.__main.acquire()
        self.__count += 1
        if self.__count < self.__threads:
            self.__main.release()
        else:
            self.__exit.release()
        self.__exit.acquire()
        self.__count -= 1
        if self.__count > 0:
            self.__exit.release()
        else:
            self.__main.release()

def example():
    def get_input(share):
        while share[0]:
            share[1] = raw_input('Please say something.\n')
            share[2].sync()
        share[3].sync()
    def do_output(share):
        while share[0]:
            share[2].sync()
            print 'You said, "%s"' % share[1]
        share[3].sync()
    share = [True, None, sync(2), sync(3)]
    thread.start_new_thread(get_input, (share,))
    thread.start_new_thread(do_output, (share,))
    import time; time.sleep(60)
    share[0] = False
    share[3].sync()

if __name__ == '__main__':
    example()
