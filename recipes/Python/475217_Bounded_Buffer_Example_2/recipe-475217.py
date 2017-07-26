from os.path import basename
from Queue import Queue
from random import random, seed
from sys import argv, exit
from threading import Thread
from time import sleep

################################################################################

class Widget:
    pass

class Stack:
    def __init__(self):
        self.__stack = list()
    def __len__(self):
        return len(self.__stack)
    def push(self, item):
        self.__stack.append(item)
    def pop(self):
        return self.__stack.pop()

################################################################################

def main():
    parse_argv()
    run_flag, buffer_queue, producer_stack, consumer_stack, print_queue = [True], Queue(argv[1]), Stack(), Stack(), Queue()
    producer_thread = Thread(target=producer, args=(run_flag, argv[3], buffer_queue, producer_stack, print_queue))
    consumer_thread = Thread(target=consumer, args=(run_flag, producer_thread, buffer_queue, consumer_stack, argv[4], print_queue))
    printer_thread = Thread(target=printer, args=(run_flag, consumer_thread, print_queue))
    producer_thread.start()
    consumer_thread.start()
    printer_thread.start()
    sleep(argv[2])
    run_flag[0] = False
    printer_thread.join()
    check_results(producer_stack , consumer_stack)

def parse_argv():
    try:
        assert len(argv) > 4
        argv[1] = abs(int(argv[1]))
        argv[2] = abs(float(argv[2]))
        assert argv[1] and argv[2]
        argv[3] = abs(float(argv[3]))
        argv[4] = abs(float(argv[4]))
        if len(argv) > 5:
            seed(convert(' '.join(argv[5:])))
    except:
        print basename(argv[0]), '<buff_size> <main_time> <prod_time> <cons_time> [<seed>]'
        exit(1)

def convert(string):
    number = 1
    for character in string:
        number <<= 8
        number += ord(character)
    return number

def check_results(producer_stack , consumer_stack):
    print 'Solution has',
    try:
        assert len(producer_stack) == len(consumer_stack)
        while producer_stack:
            assert producer_stack.pop() is consumer_stack.pop()
        print 'passed.'
    except:
        print 'failed.'

################################################################################

def producer(run_flag, max_time, buffer_queue, producer_stack, print_queue):
    while run_flag[0]:
        sleep(random() * max_time)
        widget = Widget()
        buffer_queue.put(widget)
        producer_stack.push(widget)
        print_queue.put('Producer: %s Widget' % id(widget))

def consumer(run_flag, producer_thread, buffer_queue, consumer_stack, max_time, print_queue):
    while run_flag[0] or producer_thread.isAlive() or not buffer_queue.empty():
        widget = buffer_queue.get()
        consumer_stack.push(widget)
        sleep(random() * max_time)
        print_queue.put('Consumer: %s Widget' % id(widget))

def printer(run_flag, consumer_thread, print_queue):
    while run_flag[0] or consumer_thread.isAlive() or not print_queue.empty():
        if print_queue.empty():
            sleep(0.1)
        else:
            print print_queue.get()

################################################################################

if __name__ == '__main__':
    main()
