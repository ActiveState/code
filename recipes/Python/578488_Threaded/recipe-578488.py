import cStringIO
import itertools
import Queue
import subprocess
import threading

class Transporter(object):
    def __init__(self, get, getSentinel, put, putSentinel):
        self._thread = threading.Thread(target=self.loop, args=(get, getSentinel, put, putSentinel))
        self._thread.daemon = True
        self._thread.start()

    @classmethod
    def loop(cls, get, getSentinel, put, putSentinel):
        for item in iter(get, getSentinel):
            put(item)
        put(putSentinel)

    def join(self, timeout=None):
        self._thread.join(timeout)

class Communicator(object):
    def __init__(self, write, writeSentinel, read, readSentinel):
        self._out = Queue.Queue()
        self._write = write
        self._writer = Transporter(self._out.get, (None, writeSentinel), self._onSend, (None, writeSentinel))
        self._writeSentinel = writeSentinel

        self._in = {}
        self._reader = Transporter(read, readSentinel, self._onReceive, readSentinel)
        self._readSentinel = readSentinel

        self._closing = False
        self._lock = threading.RLock()
        self._next = itertools.count().next

    def __del__(self):
        self.close()

    def put(self, command, request=True):
        with self._lock:
            deferredResult = Queue.Queue() if request else None
            if not self._closing:
                self._out.put((deferredResult, command))
            elif deferredResult:
                deferredResult.put(StopIteration())
            return deferredResult

    def close(self, timeout=None):
        self._shutdown()
        self._writer.join(timeout)
        self._reader.join(timeout)

    def _notify(self, requestId, result):
        self._in.pop(requestId).put(result)

    def _onSend(self, item):
        (deferredResult, command) = item
        requestId = None
        if deferredResult:
            requestId = self._next()
            self._in[requestId] = deferredResult

        try:
            self._write(requestId, command)
        except StopIteration as e:
            self._shutdown()
            if deferredResult:
                self._notify(requestId, e)
        except Exception as e:
            if deferredResult:
                self._notify(requestId, e)

    def _onReceive(self, item):
        if item == self._readSentinel:
            frame = item
            self._shutdown()
            self._writer.join()
            requestIds = list(self._in)
        else:
            (requestId, frame) = item
            requestIds = [requestId]

        for requestId in requestIds:
            self._notify(requestId, frame)

    def _shutdown(self):
        with self._lock:
            if self._closing:
                return
            self.put(self._writeSentinel, request=False)
            self._closing = True

class Writer(object):
    SENTINEL = None

    def __init__(self, stream):
        self._stream = stream

    def __call__(self, requestId, command):
        frame = self._compile(requestId, command)
        if frame is not None:
            try:
                self._stream.write(frame)
                self._stream.flush()
            except:
                command = self.SENTINEL
        if command == self.SENTINEL:
            try:
                self._stream.close()
            finally:
                raise StopIteration()

    def _compile(self, requestId, command):
        raise NotImplementedError()

class Reader(object):
    SENTINEL = None
    FRAME_SEPARATOR = '\x00'

    def __init__(self, stream):
        self._stream = stream
        self.__read = self._read().next

    def __call__(self):
        return self.__read()

    def _next(self):
        try:
            return self._stream.read(1)
        except:
            return ''

    def _parse(self, frame):
        raise NotImplementedError()

    def _read(self):
        self._reset()
        for character in iter(self._next, ''):
            if character != self.FRAME_SEPARATOR:
                self._buffer.write(character)
                continue
            frame = self._buffer.getvalue()
            self._reset()
            yield self._parse(frame)
        try:
            self._stream.close()
        finally:
            yield self.SENTINEL

    def _reset(self):
        self._buffer = cStringIO.StringIO()

class SubprocessSession(object):
    def __init__(self, command, writer, reader, start=True, **kwargs):
        self._command = command
        self._writer = writer
        self._reader = reader
        self._kwargs = {'stdin': subprocess.PIPE, 'stdout': subprocess.PIPE}
        self._kwargs.update(kwargs)

        self._lock = threading.RLock()
        if start:
            self.start()

    def __del__(self):
        self.close()

    def put(self, frame, request=True):
        return self._communicator.put(frame, request)

    def start(self):
        with self._lock:
            if hasattr(self, '_process'):
                return
            self._process = subprocess.Popen(self._command, **self._kwargs)
            self._communicator = Communicator(
                self._writer(self._process.stdin), self._writer.SENTINEL,
                self._reader(self._process.stdout), self._reader.SENTINEL
            )

    def close(self, timeout=None):
        with self._lock:
            if not hasattr(self, '_process'):
                return
            try:
                self._communicator.close(timeout)
            finally:
                if self._process.poll() is None:
                    self._process.kill()
                del self._process
                del self._communicator

# I use the part above as a generic utility module. A simple echo example follows:

class EchoWriter(Writer):
    def _compile(self, requestId, command):
        if command == self.SENTINEL:
            return
        return command if (requestId is None) else ('%s:%s\x00' % (requestId, command))

class EchoReader(Reader):
    def _parse(self, frame):
        requestId, frame = frame.split(':', 1)
        return (int(requestId), frame)

def run():
    from multiprocessing.pool import ThreadPool

    session = SubprocessSession('/bin/cat', EchoWriter, EchoReader)

    pool = ThreadPool(50)
    requests = pool.map(lambda j: session.put('message %d' % j), xrange(2000))
    results = pool.map(lambda r: r.get(), requests)

    print results == ['message %d' % j for j in xrange(2000)]

if __name__ == '__main__':
    run()
