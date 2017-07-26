#!/usr/bin/env python

"""asyncpipes.py: Asynchronous pipe communication using asyncore.

Extends `asyncore.file_dispatcher` to provide extra functionality for reading
from and writing to pipes. Uses the observer pattern to provide notification
of new data and closed pipes.

References:
http://code.activestate.com/recipes/576962/ [observer.py]
http://parijatmishra.blogspot.com/2008/01/writing-server-with-pythons-asyncore.html
"""

import os
from sys import stderr
from errno import EPIPE, EBADF
from asyncore import file_dispatcher
from traceback import print_exc

from observer import Observable

if __name__ == '__main__':
    import optparse
    from asyncore import loop

__version__ = '$Revision: 3742 $'.split()[1]

__usage__ = 'usage: %prog [options]'


class PipeDispatcher(Observable, file_dispatcher):
    """Dispatch pipe I/O using asyncore.

    Allows synchronous access to the pipe by delegating to the filehandle,
    though synchronous and asynchronous access should probably not be mixed.
    """
    # Event sent when the pipe is closed
    PIPE_CLOSED = 'closed'
    # Default value for maximum pipe data
    pipe_maxdata = 512

    def __init__(self, fh, map=None, maxdata=None, ignore_broken_pipe=False, logger=None, **obsopt):
        """Wrap a dispatcher around the passed filehandle.

        If `ignore_broken_pipe` is `True`, an `EPIPE` or `EBADF` error will
        call `handle_close()` instead of `handle_expt()`. Useful when broken
        pipes should be handled quietly.

        `logger` is a logger which will be used to log unusual exceptions;
        otherwise, they will be printed to stderr.
        """
        self.maxdata = maxdata if maxdata else self.pipe_maxdata
        self.__logger = logger
        if ignore_broken_pipe:
            self.__ignore_errno = [EPIPE, EBADF]
        else:
            self.__ignore_errno = []
        self.__filehandle = fh
        # Check for overduplication of the file descriptor and close the extra
        fddup = os.dup(fh.fileno())
        file_dispatcher.__init__(self, fddup, map=map)
        if (self._fileno != fddup): os.close (fddup)
        Observable.__init__(self, **obsopt)

    def __getattr__(self, attr):
        """Delegate to the filehandle."""
        return getattr(self.__filehandle, attr)

    def close(self):
        """Close the pipe and calls the _obs_notify() method."""
        if self.__filehandle:
            try:
                try:
                    file_dispatcher.close(self)
                except OSError, oe:
                    if oe.errno not in self.__ignore_errno:
                        if self.__logger: self.__logger.exception("Unusual error closing pipe dispatcher")
                        else: print_exc(file=stderr)
                try:
                    self.__filehandle.close()
                except OSError, oe:
                    if oe.errno not in self.__ignore_errno:
                        if self.__logger: self.__logger.exception("Unusual error closing pipe filehandle")
                        else: print_exc(file=stderr)
            finally:
                self.__filehandle = None
                self._obs_notify(event=self.PIPE_CLOSED)

    def readable(self):
        """Return `True` if the pipe is still open."""
        return (self.__filehandle is not None)

    def writable(self):
        """Return `True` if the pipe is still open."""
        return (self.__filehandle is not None)

    def send(self, buffer):
        """Check for closed and broken pipes when sending data."""
        if self.__filehandle:
            try:
                return file_dispatcher.send(self, buffer)
            except OSError, oe:
                if oe.errno in self.__ignore_errno: self.handle_close()
                else: self.handle_expt()
        return 0

    def recv(self, buffer_size):
        """Check for closed and broken pipes when receiving data."""
        if self.__filehandle:
            try:
                return file_dispatcher.recv(self, buffer_size)
            except OSError, oe:
                if oe.errno in self.__ignore_errno: self.handle_close()
                else: self.handle_expt()
        return ''

    def handle_close(self):
        """Call `self.close()` to close the pipe."""
        self.close()

    def handle_expt(self):
        """Print a traceback and call `handle_close()` to close the pipe."""
        if self.__logger: self.__logger.exception("Unusual exception in pipe I/O")
        else: print_exc(file=stderr)
        self.handle_close()

    def _obs_exception(self):
        """Handle an exception raised by an observer."""
        if self.__logger: self.__logger.exception("Unusual exception in pipe observer")
        else: print_exc(file=stderr)


class InputPipeDispatcher(PipeDispatcher):
    """Push data to an input pipe using asyncore."""
    def __init__(self, fh, close_when_done=False, **keywmap):
        """Wrap a dispatcher around the passed input filehandle.

        `close_when_done` closes the pipe as soon as the buffer is empty after
        the first `push_data()`.  Useful for communicating with subprocesses
        that read stdin to EOF before proceeding.
        """
        self.__buffer = None
        self.__offset = 0
        self.__close_when_done = close_when_done
        PipeDispatcher.__init__(self, fh, **keywmap)

    def readable(self):
        """Return `False`; input pipes are never readable."""
        return False

    def writable(self):
        """Return `True` if data is in the buffer and the pipe is open."""
        return PipeDispatcher.writable(self) and (self.__buffer is not None)

    def handle_write(self):
        """Write up to `maxdata` bytes to the pipe."""
        if self.writable():
            self.__offset += self.send(
                    self.__buffer[self.__offset:self.__offset+self.maxdata])
            # If the buffer is all written, empty it.
            if self.__offset >= len(self.__buffer):
                self.__buffer = None
                self.__offset = 0
                if self.__close_when_done: self.close()

    def push_data(self, data):
        """Push some data by putting it in the write buffer.

        Raise `EOFError` if the pipe is already closed.
        """
        if not PipeDispatcher.writable(self):
            raise EOFError('Input pipe closed.')
        elif self.__buffer:
            # Since we have to construct a new string, remove the already-sent data.
            self.__buffer = self.__buffer[self.__offset:] + data
        else:
            self.__buffer = data
        self.__offset = 0


class OutputPipeDispatcher(PipeDispatcher):
    """Get data from an output pipe using asyncore."""
    PIPE_DATA = 'data'
    """Event sent when new data is available in the pipe."""

    def __init__(self, fh, universal_newlines=False, **keywmap):
        """Wrap a dispatcher around the passed output filehandle.

        `universal_newlines` converts all newlines found in the data stream to
        '\n', just as in `subprocess.Popen`.
        """
        self._universal_newlines = universal_newlines
        self.__data = []
        self.__endedcr = False
        PipeDispatcher.__init__(self, fh, **keywmap)

    def writable(self):
        """Return `False`; output pipes are never writable."""
        return False

    def handle_read(self):
        """Read and queue up to `maxdata` bytes, and notify any observers."""
        if self.readable():
            data = self.recv(self.maxdata)
            if data:
                self.__data.append(data)
                self._obs_notify(self.PIPE_DATA)

    def _translate_newlines(self, data):
        data = data.replace("\r\n", "\n")
        data = data.replace("\r", "\n")
        return data

    def fetch_data(self, clear=False):
        """Return all the accumulated data from the pipe as a string.

        If `clear` is `True`, clear the accumulated data.
        """
        if self.__data:
            datastr = ''.join(self.__data)
            if clear:
                self.__data[:] = []
            if datastr and self._universal_newlines:
                # Take care of a newline split across cleared reads.
                stripnl = self.__endedcr
                if clear:
                    self.__endedcr = (datastr[-1] == '\r')
                if stripnl and datastr[0] == '\n':
                    return self._translate_newlines(datastr[1:])
                else:
                    return self._translate_newlines(datastr)
            else:
                return datastr
        else:
            return ''

    def readlines(self, clear=False):
        """Return all complete lines from the pipe as a list of strings.

        If `clear` is `True`, clear the accumulated data, but leave any
        incomplete line
        """
        datastr = self.fetch_data(clear)
        lines = datastr.splitlines(True)
        if lines[-1][-1] != '\n':
            if clear:
                self.__data[:] = [ lines[-1] ]
            return lines[0:-1]
        return lines


if __name__ == '__main__':
    class TestAsyncPipe:
        def __init__(self, maxprint, lineterm, loops, maxwrite, maxread):
            self._maxprint = maxprint
            self._lineterm = lineterm
            self._loops = loops
            rp, wp = os.pipe()
            self._inpipe = InputPipeDispatcher(os.fdopen(wp, 'wb'),
                    maxdata=maxwrite)
            self._outpipe = OutputPipeDispatcher(os.fdopen(rp, 'rb'),
                    maxdata=maxread, universal_newlines=(lineterm != '\n'))
            self._inpipe.obs_add(self)
            self._outpipe.obs_add(self)

        def _printdata(self, data):
            if not data:
                printable = ''
            elif len(data) > self._maxprint + 1:
                printable = ': %r' % ('%s...%s' % (data[:self._maxprint], data[-1]))
            else:
                printable = ': %r' % data
            print '%d bytes received%s' % (len(data), printable)

        def handle_notify(self, pipe, event):
            if event == OutputPipeDispatcher.PIPE_DATA:
                data = pipe.fetch_data(clear=False)
                self._printdata(data)
                if data.endswith('\n'):
                    self._loops -= 1
                    if self._loops:
                        data = pipe.fetch_data(clear=True).strip()
                        self._inpipe.push_data(data + self._lineterm)
                    else:
                        self._inpipe.close()
                        self._outpipe.close()
            else:
                print '%s %s' % (pipe.__class__, event)


    optparser = optparse.OptionParser(usage=__usage__, version=__version__)
    optparser.disable_interspersed_args()
    optparser.add_option('--data', default='0123456789',
            help='Data string to be sent [%default]')
    optparser.add_option('--copies', type=int, metavar='N', default=1,
            help='Repeat the data N times (to test large transfers) [%default]')
    optparser.add_option('--maxread', type='int', metavar='BYTES', default=1024,
            help='Maximum data to read in each chunk [%default]')
    optparser.add_option('--maxwrite', type='int', metavar='BYTES', default=1024,
            help='Maximum data to write in each chunk [%default]')
    optparser.add_option('--loops', type='int', metavar='N', default=5,
            help='Number of loops to execute [%default]')
    optparser.add_option('--lineterm', type='choice', metavar='TERM', choices=['CR','CRLF','LF'],
            default='LF', help='Line terminator to send: CR, CRLF, or LF [%default]')
    (options, args) = optparser.parse_args()

    # Translate the line terminator to an escape sequence.
    lineterm = {'CR':'\r', 'CRLF':'\r\n', 'LF':'\n'}[options.lineterm]
    pipe_handler = TestAsyncPipe(len(options.data), lineterm, options.loops, options.maxwrite, options.maxread)
    pipe_handler._inpipe.push_data(options.data * options.copies + lineterm)
    loop()
