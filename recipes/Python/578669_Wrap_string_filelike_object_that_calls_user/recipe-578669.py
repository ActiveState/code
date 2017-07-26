import cStringIO as StringIO

class ReadCallbackStream(object):
    """Wraps a string in a read-only file-like object, but also calls
    callback(num_bytes_read) whenever read() is called on the stream. Used for
    tracking upload progress. Idea taken from this StackOverflow answer:
    http://stackoverflow.com/a/5928451/68707
    """
    def __init__(self, data, callback):
        self._len = len(data)
        self._io = StringIO.StringIO(data)
        self._callback = callback

    def __len__(self):
        return self._len

    def read(self, *args):
        chunk = self._io.read(*args)
        if len(chunk) > 0:
            self._callback(len(chunk))
        return chunk
