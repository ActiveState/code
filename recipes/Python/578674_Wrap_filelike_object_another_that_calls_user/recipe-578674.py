import cStringIO as StringIO
import os

class ReadCallbackStream(object):
    """Wraps a file-like object in another, but also calls a user
    callback with the number of bytes read whenever its `read()` method
    is called. Used for tracking upload progress, for example for a
    progress bar in a UI application. Idea taken from ActiveState Code Recipe:
    http://code.activestate.com/recipes/578669-wrap-a-string-in-a-file-like-object-that-calls-a-u/
    """
    def __init__(self, file_like, callback):
        self.file_like = file_like
        self._callback = callback

    def __len__(self):
        raise NotImplementedError()

    def read(self, *args):
        chunk = self.file_like.read(*args)
        if len(chunk) > 0:
            self._callback(len(chunk))
        return chunk

class ReadCallbackString(ReadCallbackStream):
    def __init__(self, data, callback):
        super(ReadCallbackString, self).__init__(StringIO.StringIO(data), callback)
        self._len = len(data)

    def __len__(self):
        return self._len

class ReadCallbackFile(ReadCallbackStream):
    def __init__(self, filename, callback):
        super(ReadCallbackFile, self).__init__(open(filename), callback)

    def __len__(self):
    	curpos = self.file_like.tell()
    	self.file_like.seek(0, os.SEEK_END)
    	file_length = self.file_like.tell() - curpos
    	self.file_like.seek(curpos, os.SEEK_SET)
        return file_length


if __name__ == '__main__':
    import json
    import urllib2

    def callback(num_bytes_read):
        print 'callback:', num_bytes_read, 'bytes read'

    data = 'x' * 20000
    stream = ReadCallbackString(data, callback)
    request = urllib2.Request('http://httpbin.org/post', stream)
    f = urllib2.urlopen(request)
    response = json.loads(f.read())
    print 'httpbin.org said we POSTed', len(response['data']), 'bytes'

    # create a real file and repeat process
    print
    filename = 'testfile'
    with open(filename, 'w') as testfile:
        testfile.write(data)

    stream = ReadCallbackFile(filename, callback)
    request = urllib2.Request('http://httpbin.org/post', stream)
    f = urllib2.urlopen(request)
    response = json.loads(f.read())
    print 'httpbin.org said we POSTed', len(response['data']), 'bytes'
