from os.path import basename
from Queue import Queue
from random import random
from sys import argv, exit
from threading import Thread
from time import sleep

# for creating widgets
class Widget:
    pass

# for creating stacks
class Stack:
    def __init__(self):
        self.__stack = list()
    def __len__(self):
        return len(self.__stack)
    def push(self, item):
        self.__stack.append(item)
    def pop(self):
        return self.__stack.pop()

# provides an outline for the execution of the program
def main():
    # check and parse the command line arguments
    parse_sys_argv()
    # setup the variables used by the threads
    run_flag = [True]
    queue = Queue(argv[1])
    send = Stack()
    recv = Stack()
    # start the threads
    producer = Thread(target=produce, args=(run_flag, queue, send))
    consumer = Thread(target=consume, args=(run_flag, queue, recv, producer))
    producer.start()
    consumer.start()
    # let the threads do their work
    sleep(argv[2])
    run_flag[0] = False
    consumer.join()
    # verify that the solution was valid
    calculate_results(send, recv)

# parses and checks the command line arguments
def parse_sys_argv():
    try:
        # there should be two command line arguments
        assert len(argv) == 3
        # convert <buf_size> and check
        argv[1] = abs(int(argv[1]))
        assert argv[1] > 0
        # convert <run_time> and check
        argv[2] = abs(float(argv[2]))
        assert argv[2] > 0
    except:
        # print out usage information
        print basename(argv[0]),
        print '<buf_size> <run_time>'
        # exits the program
        exit(1)

# called by the producer thread
def produce(run_flag, queue, send):
    while run_flag[0]:
        # simulate production
        sleep(random())
        # put widget in buffer
        item = Widget()
        queue.put(item)
        send.push(item)

# called by the consumer thread
def consume(run_flag, queue, recv, producer):
    # consume items while running
    while run_flag[0]:
        do_consume(queue, recv)
    # empty the queue to allow maximum room
    while not queue.empty():
        do_consume(queue, recv)
    # wait for the producer to end
    producer.join()
    # consume any other items that might have been produced
    while not queue.empty():
        do_consume(queue, recv)

# executes one consumption operation
def do_consume(queue, recv):
    # get a widget from the queue
    recv.push(queue.get())
    # simulate consumption
    sleep(random())

# verifies that send and recv were equal
def calculate_results(send, recv):
    print 'Solution has',
    try:
        # make sure that send and recv have the same length
        assert len(send) == len(recv)
        # check all of the contents of send and recv
        while send:
            # check the identity of the items in send and recv
            assert send.pop() is recv.pop()
        print 'passed.'
    except:
        print 'failed.'

# starts the program
if __name__ == '__main__':
    main()
