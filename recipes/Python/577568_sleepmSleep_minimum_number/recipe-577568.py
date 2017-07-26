from time import time, sleep

def sleep_min(delay):
    accum = 0
    remainder = delay
    while accum < delay:
        begin = time()
        sleep(remainder)
        end = time()
        slept = end - begin
        accum += slept
        remainder -= slept
