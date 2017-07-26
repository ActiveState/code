from threading import Thread
import time

def worker(n, emit):
    time.sleep(n)
    emit(n)
    print(n)

def sleep_sort(s):
    # Idea inspired by: http://dis.4chan.org/read/prog/1295544154
    result = []
    emit = result.append
    threads = [Thread(target=worker, args=(x, emit)) for x in s]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

if __name__ == '__main__':
    import random

    s = list(range(10))
    random.shuffle(s)
    print ('Shuffled:', s)
    print ('Sorted:', sleep_sort(s))
