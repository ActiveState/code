import time

class TerseLogger:

    def __init__(self, max_silent_time=60, display_time=False):

        self.prev_msg = None
        self.last_msg_time = 0
        self.max_silent_time = max_silent_time

        self.display_time = display_time

    # yeah - emit is actually a bad name because it doesn't emit every time...
    def emit(self, msg):

        now = time.time()
        # actually print message if either a) or b) applies
        # a) it is different from previous message
        # b) max_silent_time seconds have passed since last message

        if self.prev_msg != msg \
               or now - self.last_msg_time >= self.max_silent_time:

            if self.display_time:
                print "%d %s" % (now, msg)
            else:
                print msg

            self.prev_msg = msg
            self.last_msg_time = now


if __name__ == '__main__':

    obj = TerseLogger(display_time=True)

    messages = ('cat', 'dog', 'cat', 'cat', 'penguin')

    print "message is not printed if it was the same as previous message"
    for msg in messages:
        obj.emit(msg)

    obj = TerseLogger(1, display_time=True)

    print ("all messages are printed because max_silent_time "
           "was set to 1 second and we sleep 2 seconds after each iteration")
    for msg in messages:
        obj.emit(msg)
        time.sleep(2)
