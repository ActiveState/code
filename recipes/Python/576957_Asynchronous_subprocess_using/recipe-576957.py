#!/usr/bin/env python

"""asyncsubproc.py: Asynchronous subprocess communication using asyncore.

The `AsyncPopen` class wraps the I/O pipes from `Popen` in asynchronous
dispatchers, providing asynchronous communication with the subprocess using
`asyncore.loop()` to read and write in parallel with other I/O.  The
`SubprocessExecutor` class wraps `AsyncPopen` in an `Executor`, allowing
inline subprocess execution using a generator.

Full-duplex Communication:
Data that the subprocess writes might not be made available to the parent until
the subprocess calls `flush()` or exits; thus, a parent which attempts to write
data, read a response, and then write new data contingent on the response might
find itself deadlocked. There seems to be no way for the parent process to
force flushing of the subprocess output; changing the value of the `bufsize`
parameter to `Popen()` to zero (or any other value) doesn't do it, and
`asyncore.file_dispatcher` already sets `O_NONBLOCK` on the pipes.

Subprocess Exit:
Detecting subprocess exit while avoiding zombie subprocesses can be tricky in
asynchronous code. Calling `wait()` on a subprocess would block, leaving three
alternatives for checking for subprocess exit:
    1) Exit the asynchronous select loop (e.g. `asyncore.loop()`) occasionally
to call `poll()` on any unterminated subprocesses. This requires maintaining a
list of all unterminated subprocess objects, along with any context needed to
handle the subprocess exit.
    2) Set a handler for `SIGCHLD` which calls `os.waitpid(-1, os.WNOHANG)`,
and then use the return value to locate the asynchronous process object and
handle the subprocess exit. This must be done in a loop to avoid missing
consolidated signals, requires maintaining a list of all unterminated
subprocesses, and is limited by reentrancy restrictions on signal handlers.
    3) Check for `stdout` and `stderr` to both be closed, which can be done as
part of the asynchronous loop which reads data. This requires that at least one
of `stdout` and `stderr` be a pipe, but an asynchronous subprocess is probably
unnecessary in the first place if neither is a pipe. There is no absolute
guarantee that the subprocess has exited when `stdout` and `stderr` have
closed, but once they have, no more data is coming. However, because `wait()`
is not being called on the subprocesses, special care has to be taken to avoid
leaving zombie subproceses. There are again three alternatives:
    a) Set `SIGCHLD` to `SIG_IGN`. This should work on most varieties of UNIX
including Mac OS X. However, it prevents collecting the exit status of the
subprocess; `poll()` will return `None` and `wait()` will raise an `OSError`
exception.
    b) Set a handler for `SIGCHLD` as in solution (2) above; if this is to be
implemented, it may be better to simply implement solution (2) rather than
waiting for the output pipes to close in the first place.
    c) Call `wait()` on the subprocess after stdout and stderr are closed.
While this will block (briefly), it should be reasonably safe unless the
subprocess does something very unusual.
    `SubprocessExecutor` waits for `stdout` and `stderr` to both be closed, and
then calls `wait()` on the subprocess if no handler for `SIGCHLD` is set.

References:
http://code.activestate.com/recipes/577600/ [queued SIGALRM alarms]
http://code.activestate.com/recipes/576965/ [event-based asynchronous pattern]
http://code.activestate.com/recipes/576967/ [asynchronous pipe I/O]
"""

import os
import sys
import signal
import threading
from traceback import print_exc
from subprocess import Popen, PIPE
from logging import ERROR, INFO

import alarm
from asyncpipes import PipeDispatcher, InputPipeDispatcher, OutputPipeDispatcher
from worker import Executor
from observer import Observable

if __name__ == '__main__':
    import optparse
    from asyncore import loop
    from string import digits
    from time import sleep
    from worker import execute, ExecutionQueue

__version__ = '$Revision: 3414 $'.split()[1]

__usage__ = 'usage: %prog [options] [data]'


class AsyncPopen(Observable, Popen):
    """An extension to Popen which creates a subprocess with asynchronous
    pipes for input and output. Pipe output can be read using an Observer
    pattern while asyncore.loop() is run.

    Also contains additional small extensions, such as a subprocess timeout
    and a fix to handling of signals for subprocesses.
    """
    def __init__(self, argv, map=None, timeout=None, close_when_done=True,
            stdin=PIPE, stdout=PIPE, stderr=PIPE, preexec_fn=None, bufsize=0, **popen_keyw):
        """Accepts all the same arguments and keywords as `subprocess.Popen`.
        Input or outputs specified as `PIPE` (now the default) for are wrapped
        in an asynchronous pipe dispatcher.

        The timeout is used to create an alarm, which can be cancelled by
        calling `cancel_timeout()`, `communicate()`, `wait()` or `kill()`.
        """
        Observable.__init__(self)
        self._map = map
        # Create the subprocess itself, wrapping preexec_fn in the clear_signals call
        Popen.__init__(self, argv, preexec_fn=lambda: self.clear_signals(preexec_fn),
                stdin=stdin, stdout=stdout, stderr=stderr, **popen_keyw)
        # Set the timeout on the subprocess.  If it fails, ignore the failure.
        try:
            fto = float(timeout)
            self._alarmobj = alarm.alarm(fto, self.kill) if fto > 0 else None
        except:
            self._alarmobj = None
        # Wrap the pipe I/O. Sets the Popen and pipe buffer sizes the same; perhaps not optimal.
        if stdout == PIPE:
            self.stdout = OutputPipeDispatcher(self.stdout, map=map, ignore_broken_pipe=True,
                    universal_newlines=self.universal_newlines, maxdata=bufsize)
            self.stdout.obs_add(self._pipe_event)
        if stderr == PIPE:
            self.stderr = OutputPipeDispatcher(self.stderr, map=map, ignore_broken_pipe=True,
                    universal_newlines=self.universal_newlines, maxdata=bufsize)
            self.stderr.obs_add(self._pipe_event)
        if stdin == PIPE:
            self.stdin = InputPipeDispatcher(self.stdin, map=map, ignore_broken_pipe=True,
                    close_when_done=close_when_done, maxdata=bufsize)
            self.stdin.obs_add(self._pipe_event)

    def cancel_timeout(self, logger=None):
        if not self._alarmobj: return
        try:
            alarm.cancel(self._alarmobj)
        except:
            if logger: logger.debug("Error canceling child PID %d alarm" % child.pid, exc_info=1)
        finally:
            self._alarmobj = None

    def wait(self, logger=None):
        returncode = Popen.wait(self)
        self.cancel_timeout(logger=logger)
        return returncode

    @staticmethod
    def clear_signals(preexec_fn):
        """Wraps any preexec_fn in order to clear any signal handlers."""
        for s in range(1, signal.NSIG):
            try:
                if s not in [signal.SIGKILL, signal.SIGSTOP]: signal.signal(s, signal.SIG_DFL)
            except:
                pass
        if callable(preexec_fn): preexec_fn()

    def kill(self):
        """Kill the child process with extreme prejudice."""
        try:
            if self.returncode is None: os.kill(self.pid, signal.SIGKILL)
        finally:
            self.cancel_timeout()

    def fetch_output(self, clear=True):
        """Fetch data from the subprocess output pipes.

        An output file not set to a pipe returns an empty string.
        """
        outdata = self.stdout.fetch_data(clear) if self.stdout is not None else ''
        errdata = self.stderr.fetch_data(clear) if self.stderr is not None else ''
        return outdata, errdata

    def output_closed(self):
        """Return true if both subprocess output pipes are closed.

        Can be used to detected the termination of the subprocess. An output
        file not sent to a pipe is ignored.
        """
        outread = self.stdout.readable() if self.stdout is not None else False
        errread = self.stderr.readable() if self.stderr is not None else False
        return not (outread or errread)

    def _pipe_event(self, observed, event):
        """Forward events on the pipes. The forwarded events contain the pipe
        event and the pipe itself as a two-element tuple."""
        self._obs_notify((event, observed))


class SubprocessExecutor(Executor):
    """Executes subprocesses, reading and writing data using `asyncore`.

    For each subprocess to be created, the generator must yield either the
    object to be passed to the `argv` argument of the `Popen` constructor,
    or a dictionary containing a required `argv` key, an optional `input` key
    containing a string to be written to `stdin` of the subprocess, and keys
    corresponding to the keyword parameters to `AsyncPopen` (the same keywords
    as the `child_spawn()` method).

    Once the subprocess has exited, the executor will call `send()` on the
    generator, passing a 4-element tuple containing the data read from
    `stdout` and `stderr`, the exit status returned by `Popen.poll()`, and the
    pid of the subprocess. The generator can then yield the parameters for
    another subprocess.
    """
    def __init__(self, generator, exc_handler=print_exc, logger=None, **async_popen_keyw):
        """Initialize a subprocess executor.

        Additional keyword parameters to this constructor (usually passed
        through the decorator) will be passed to `AsyncPopen`.
        """
        Executor.__init__(self, generator, exc_handler)
        self._logger = logger
        self.__async_popen_dict = async_popen_keyw
        self.__current_child = None

    def _execute(self, logger=None, **async_popen_keyw):
        """Iterate the generator to completion (in the calling thread).

        The generator must yield the parameters for the first subprocess,
        which will be passed to `_spawn()`.

        Additional keyword parameters passed to this object when called will
        be passed to `AsyncPopen` (and override values passed to this object's
        constructor).
        """
        self.__async_popen_dict.update(async_popen_keyw)
        if logger is not None: self._logger = logger
        # Get the command to be executed from the generator
        self.__coerce_and_spawn(self.next())

    def _pipe_closed(self, observed, event):
        """Called when one of the output pipes (stdout or stderr) is closed.

        Once both are closed, declare the subprocess finished and call
        `_child_exit()`.
        """
        if observed.output_closed(): self._child_exit(observed)

    def _child_exit(self, child):
        """Called once `stdout` and `stderr` are both closed.

        Cleans up the subprocess, and then passes the subprocess results tom
        the generator by calling `send()`.  If the generator yields parameters
        for another subprocess, calls `_child_spawn()`.
        """
        self.__current_child = None
        # Close stdin for the child, so that it knows it won't be getting more data
        try:
            if child.stdin is not None: child.stdin.close()
        except:
            if self._logger: self._logger.debug("Error closing stdin for PID %d" % child.pid, exc_info=1)
        # Wait for the child if there's no signal handler
        if signal.getsignal(signal.SIGCHLD) == signal.SIG_DFL:
            try:
                # This will cancel the alarm
                returncode = child.wait(logger=self._logger)
            except:
                if self._logger: self._logger.debug("Error waiting for child PID %d" % child.pid, exc_info=1)
                else: print_exc(file=sys.stderr)
        else:
            child.cancel_timeout(logger=self._logger)
            # This next will return None unless an exit status injector has been set up.
            returncode = child.poll()
        # Extract the result from the child process; and move on with the executor
        try:
            outdata, errdata = child.fetch_output()
            child_result = (outdata, errdata, returncode, child.pid)
            if self._logger: self._logger.debug("PID %d exited with code %s" % (child.pid, returncode))
            self.__coerce_and_spawn(self.send(child_result))
        except:
            self.throw(*sys.exc_info())

    def close(self):
        """Kill the subprocess when closing the generator."""
        child = self.__current_child
        if child:
            try:
                child.kill()
            except:
                if self._logger: self._logger.exception("Error killing child PID %d" % child.pid)
                else: print_exc(file=sys.stderr)
            else:
                self.__current_child = None
        Executor.close(self)

    def __coerce_and_spawn(self, arg):
        """Coerce the argument into a call to `_child_spawn()`"""
        try:
            self._child_spawn(**arg)
        except:
            self._child_spawn(argv=arg)

    def _child_spawn(self, argv=None, input=None, **async_popen_keyw):
        """Create the subprocess and send the data to the input pipe. Called
        with the value(s) yielded by the generator.

        If a subprocess is to be spawned, the `argv` keyword must be supplied
        with a non-empty value. The value passed to the `input` keyword will
        be written to `stdin` of the subprocess.

        Additional keyword parameters passed to this method will
        be passed to `AsyncPopen` (and override values passed to this object's
        constructor).
        """
        if self.stopped(): return
        # Merge the keyword arguments together to pass to AsyncPopen
        async_popen_dict = self.__async_popen_dict.copy()
        async_popen_dict.update(async_popen_keyw)
        if input: async_popen_dict["stdin"] = PIPE
        # Create the subprocess itself
        if self._logger: self._logger.debug("Spawning subprocess %s" % argv)
        self.__current_child = AsyncPopen(argv, **async_popen_dict)
        if self._logger: self._logger.debug("Spawned subprocess %s with PID %d" % (argv, self.__current_child.pid))
        # Listen for both output pipes to close, and push the data to stdin
        self.__current_child.obs_add(self._pipe_closed, criteria=PipeDispatcher.PIPE_CLOSED)
        if input: self.__current_child.stdin.push_data(str(input))


if __name__ == '__main__':
    def printdata(data, pid, channame):
        print '[%d] %s %d bytes received: %r' % (pid, channame, len(data), data)

    execq = ExecutionQueue()

    @execute(execq, SubprocessExecutor)
    def spawn_child(argv, data, child, loops):
        """Spawn a cascade of subprocesses."""
        for lp in range(1, loops + 1):
            (stdout, stderr, stat, pid) = yield {'argv': argv, 'input': '%s%s' % (data, '\n')}
            printdata(stdout, pid, 'stdout')
            printdata(stderr, pid, 'stderr')
            print "Loop %d child %d [%d] exited with status %s" % (lp, child, pid, stat)
            if stat == 0 and data == stdout.rstrip()[::-1]: data = stdout[:-1]

    def run_child(pause, exitstat):
        """Run the subprocess code; a simple string inverter."""
        line = sys.stdin.readline().strip()
        sleep(pause / 2.0)
        # Write and close both pipes to show that it waits for exit anyway.
        print line[::-1]
        print >>sys.stderr, line
        sys.stdout.close()
        sys.stderr.close()
        sleep(pause / 2.0)
        sys.exit(exitstat)

    optparser = optparse.OptionParser(usage=__usage__, version=__version__)
    optparser.disable_interspersed_args()
    optparser.add_option('--loops', type='int', metavar='N', default=3,
            help='Number of times to iterate each child [%default]')
    optparser.add_option('--children', type='int', metavar='N', default=3,
            help='Number of children to spawn [%default]')
    optparser.add_option('--timeout', type='float', metavar='SECONDS', default=10.0,
            help='Maximum time subprocess is allowed to run [%default sec]')
    optparser.add_option('--no-signal', dest='nosignal', action='store_true', default=False,
            help='Ignore signals from child processes.')
    childopts = optparse.OptionGroup(optparser, 'Child options')
    childopts.add_option('--child', action='store_true', help=optparse.SUPPRESS_HELP)
    childopts.add_option('--pause', type='float', metavar='SECONDS', default=2.0,
            help='Time to pause in the child process [%default sec]')
    childopts.add_option('--exitstat', type='int', metavar='STATUS', default=0,
            help='Child exit status [%default]')
    optparser.add_option_group(childopts)
    (options, args) = optparser.parse_args()

    if options.child:
        run_child(options.pause, options.exitstat)
    else:
        # Run the parent process code: start the first child and send data.
        if options.nosignal: signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        sys.argv.insert(1, '--child')
        # Create and queue the children, and then loop asyncore
        data = ' '.join(args) if len(args) else digits
        for ch in range(1, options.children + 1):
            spawn_child(sys.argv, data, ch, options.loops)(timeout=options.timeout)
        loop()
        os.system('ps -ef')
