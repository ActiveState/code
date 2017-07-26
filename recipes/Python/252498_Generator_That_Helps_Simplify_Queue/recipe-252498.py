def iterQueue(queue, sentinel):
    """Iterate over the values in queue until sentinel is reached."""
    while True:
        value = queue.get()
        if value != sentinel:
            yield value
        else:
            return
