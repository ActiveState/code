import time

class memcached_queue_context():
    "A context manager for queuing operations per key via memcached"

    poll_interval = 0.005 # in seconds

    def __init__(self, memcache_client, key_base):
        self.mc = memcache_client
        self.key_base = key_base

        self.queue_push_key = self.key_base + "-push"
        self.queue_wait_key = self.key_base + "-wait"

    def __enter__(self):
        # initialize the queues if needed
        self.mc.add(self.queue_push_key, '1')
        self.mc.add(self.queue_wait_key, '1')

        # take a number
        index = self.mc.incr(self.queue_push_key) - 1

        # poll the queue until your number comes up
        while True:
            idx = int(self.mc.get(self.queue_wait_key)) # int() is critical!!!
            if not idx < index:
                break
            time.sleep(self.poll_interval)
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        # advance the queue
        self.mc.incr(self.queue_wait_key)
        return False
