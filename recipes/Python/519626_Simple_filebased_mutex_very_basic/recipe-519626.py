import os

class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.fd = None
        self.pid = os.getpid()

    def acquire(self):
        try:
            self.fd = os.open(self.filename, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            # Only needed to let readers know who's locked the file
            os.write(self.fd, "%d" % self.pid)
            return 1    # return ints so this can be used in older Pythons
        except OSError:
            self.fd = None
            return 0

    def release(self):
        if not self.fd:
            return 0
        try:
            os.close(self.fd)
            os.remove(self.filename)
            return 1
        except OSError:
            return 0

    def __del__(self):
        self.release()

def main():
    lock = FileLock("lock.file")
    while 1:
        if lock.acquire():
            raw_input("acquired lock. Press ENTER to release:")
            lock.release()
            raw_input("released lock. Press ENTER to retry:")
        else:
            raw_input("Unable to acquire lock. Press ENTER to retry:")

if __name__ == "__main__":
    main()
