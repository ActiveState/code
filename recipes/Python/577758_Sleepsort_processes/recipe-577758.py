import os
import time

def sleepsort(l):
    """Another dumb sorting algorithm."""
    pids = []
    def reap():
        while pids:
            os.waitpid(pids.pop(), 0)
    # Setup communication.
    startr, startw = os.pipe()
    resr, resw = os.pipe()
    try:
        for i, x in enumerate(l):
            pid = os.fork()
            if pid == 0:
                # Wait for parent process to signal start.
                os.read(startr, 1)
                time.sleep(x)
                # Notify the parent process.
                os.write(resw, str(i).encode("ascii") + b" ")
                # Goodbye.
                os._exit(0)
            else:
                pids.append(pid)
        # Start the sleeps.
        os.write(startw, b"x" * len(l))
        os.close(startw)
        startw = -1
        reap()
        os.close(resw)
        resw = -1
        # Read results.
        data = []
        while True:
            d = os.read(resr, 4096)
            if len(d) == 0:
                break
            data.append(d)
    finally:
        os.close(startr)
        if startw > 0:
            os.close(startw)
        os.close(resr)
        if resw > 0:
            os.close(resw)
        reap()
    return [l[int(c)] for c in b"".join(data)[:-1].split(b" ")]

if __name__ == "__main__":
    print(sleepsort([10, 9, 7.3, 7, 6, .2, .4, 3, 2, 1.5]))
