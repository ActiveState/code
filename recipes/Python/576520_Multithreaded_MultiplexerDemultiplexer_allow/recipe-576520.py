# Author: David Decotigny, Oct 1, 2008
#  @brief Multiplexer for parallel transactions over a single data
#  channel.  This is like a pipe on which we provide a multithreaded
#  request/response messaging system. This system allows multiple
#  threads to issue several requests in parallel: they are treated in
#  parallel on the receiving side and the responses are sent back to
#  their respective requesting thread. The exceptions are correctly
#  transferred: the _trace member of the exception object will
#  indicate the traceback (as text).
#
#  The basic synopsis is:
#    - call Mux::transaction(*args, **kwds) from a "sender" thread
#    - the transaction is sent to the Demux via the channel
#    - DeMux::process_transaction(*args, **kwds) gets called by another thread,
#      on the other side of the channel (in general in
#      another process/machine)
#    - the result/exception of process_transaction() is sent back to the
#      sender via the channel
#    - Mux::transaction() on the sender returns or raises the exception
#      raised by DeMux::process_transaction()
#
#  The user code of this module has to override the
#  DeMux::process_transaction() method for the whole system to be
#  useful.
#
#  This module makes the following assumptions on the channel used to
#  transmit the requests/responses:
#  - the channel is bidirectional: both parties can send and receive data on it
#  - the channel can transmit arbitrary serializable python objects
#  - the channel consists of 2 endpoints having the same API: one
#    endpoint for the Multiplexer, one endpoint for the DeMultiplexer
#  - the endpoints of the channel have the following methods:
#      fileno(): return a file descriptor suitable for select/poll of data
#                ready to be received in non-blocking mode (at least for the
#                first byte)
#      send(data): send the given python data to the receiving party
#      data = recv(): wait for python data from the sending party and return it
#      close(): close the endpoint in both send/receive directions
#  - send() is multithread-safe
#
#  To achieve parallel handling of "simultaneous" requests, the
#  demultiplexer handles each request in a separate thread: either the
#  threads are created on demand (nworkers = None), or a pool of
#  pre-allocated threads is used (nworkers = integer). To manage the
#  interleaving of the transactions, each transaction has its own ID,
#  the "xid".

import sys, os, threading, Queue, itertools, traceback, select, struct
import cPickle as pickle # Only for SimpleChannelEndpoint

__all__ = ["Mux", "DeMux", "ChannelPair"]


## Magic token to mark the end of job submission by the DeMux
SENTINEL = "QUIT"
def is_sentinel(obj):
    """Predicate True when a DeMux worker thread receives a
    "terminate" order from the DeMux"""
    return type(obj) is str and obj == SENTINEL


class ReceiverThread(threading.Thread):
    """Generic wrapper class to wait for data from a channel:
    handle_message() is called for each data received. Provides a
    stop() method to stop receiving the data. This is a thread
    object: call start() to start it"""
    def __init__(self, channel, *args, **kwds):
        """
        \param channel is a Channel endpoint (fileno/recv/close
        methods expected)
        """
        threading.Thread.__init__(self, *args, **kwds)
        self._channel = channel
        self.__terms  = os.pipe()

        self._recv = channel.recv
        self._send = channel.send

    def run(self):
        """
        Wait for either a call to stop() or for a data to be available
        on the channel and then call handle_message. And loop over.
        """
        # Initialize poll()
        fd        = self._channel.fileno()
        waitset   = select.poll()
        eventmask = select.POLLIN | select.POLLERR \
                    | select.POLLHUP | select.POLLPRI
        waitset.register(fd, eventmask)
        waitset.register(self.__terms[0], eventmask)

        while 1:
            exit_loop = False
            for fd_, evt in waitset.poll():
                if fd_ != fd:
                    # Received sthg on the __terms pipe
                    exit_loop = True
                    break
                if evt != select.POLLIN:
                    # Receive something on the channel, but not a normal
                    # data (probably a HUP)
                    exit_loop = True
                    break

            if exit_loop:
                break

            # Error while receiving => term thread
            data = self._recv()

            # Call handle_message (dump the exceptions, but ignore them)
            try:
                self.handle_message(data)
            except:
                traceback.print_exc()
        # End while

    def handle_message(self, message):
        """Method to override: called each time a message is received"""
        raise NotImplementedError("Children classes expected to override it")

    def stop(self):
        """Stop receiving data. Waits until the thread is
        terminated. DO NOT CALL THIS from inside handle_message()"""
        os.write(self.__terms[1], "TERMINATION")
        self._channel.close()
        self.join()


class Mux(ReceiverThread):
    """Thread that multiplexes calls to the transaction() method on
    the given channel"""
    
    def __init__(self, channel):
        """
        \param channel is a Channel endpoint (fileno/recv/close
        methods expected)
        """
        ReceiverThread.__init__(self, channel)
        self.__lock  = threading.Lock()
        self.__waitq = dict()
        self.__idgen = itertools.count(42)

    def transaction(self, *args, **kwds):
        """Call this method to send the given args on the wire and
        wait for a response"""
        evt = threading.Event(self.__lock)

        # Allocate a transaction ID
        self.__lock.acquire()
        try:
            xid = self.__idgen.next()
            assert xid not in self.__waitq
            self.__waitq[xid] = [evt, None] # If except: means MUX stopped
        except AttributeError:
            raise EOFError("MUX has been stopped.")
        finally:
            self.__lock.release()

        # Send the request
        self._send((xid, args, kwds))

        # Wait for the answer
        evt.wait()

        # Return the answer/raise the exception to the caller
        self.__lock.acquire()
        try:
            # Retrieve the result
            try:
                result = self.__waitq[xid][1]
            except (AttributeError, IndexError):
                raise EOFError("MUX has been stopped.")
            except:
                print "EX", self.__waitq

            # Work done
            del self.__waitq[xid]

            # Reformat the result
            xid_, result_ = result
            assert xid_ == xid, \
                   "Expected txn id %s != received (%s)" % (xid, xid_)
            
            status, details = result_
            if status == "OK":
                return details
            elif status == "EXCEPTION":
                raise details
            else:
                raise RuntimeError("Invalid status %s !" % repr(status))
            return result
        finally:
            self.__lock.release()

    def run(self):
        """Listen to the messages coming from the endpoint and
        dispatch them to the threads which sent them"""
        try:
            ReceiverThread.run(self)
        except:
            traceback.print_exc()
        
        # If we're here, it means that a stop has been requested:
        # unblock _all_ the waiting caller threads and force them
        # to fail in transaction()
        self.__lock.acquire()
        try:
            for xid, slot in self.__waitq.iteritems():
                del slot[1] # Force IndexError on the waiting threads
                slot[0].set()
            del self.__waitq # Force AttributeError on next transaction()
        finally:
            self.__lock.release()

    def handle_message(self, msg):
        """Needed by the ReceiverThread object: dispatch the messages
        to the caller threads"""
        xid, result = msg
        self.__lock.acquire()
        try:
            slot = self.__waitq[xid]
            slot[1] = msg
            slot[0].set() # wake up the caller thread
        finally:
            self.__lock.release()


class DeMux(ReceiverThread):
    """Thread that demultiplexes transactions coming from a
    multiplexer, and calls process_transaction() for each of them. The
    transactions are processed in parallel in different worker
    threads. The worker threads are either consisting in a pool of
    threads (when nworkers is not None), or are created on-demand when
    requests arrive (when nworkers is None)"""
    
    __lock     = None # Lock object
    __workq    = None # Queue object or None (in on-demand mode)
    __nworkers = None # Specified size of the pool of threads
    __workers  = None # Either a list of threads (pool) or a dict xid->thread
                      # (in on-demand mode)
    
    def __init__(self, channel, nworkers = None):
        """
        \param channel is a Channel endpoint (fileno/recv/close
        methods expected)
        \param nworkers (integer) number of threads in the pool able
        to process the transaction requests, or None when threads have
        to be created on demand
        """
        ReceiverThread.__init__(self, channel)
        self.__nworkers = nworkers
        self.__lock     = threading.Lock()
        if nworkers is not None:
            self.__workers = []
            self.__workq   = Queue.Queue()
            for idworker in range(nworkers):
                thr = threading.Thread(target=self._pool_work)
                self.__workers.append(thr)
                thr.start()
        else:
            self.__workers = dict()

    def handle_message(self, msg):
        """Required by ReceiverThread"""
        xid, args, kwds = msg
        if self.__nworkers is not None:
            # In pool mode: send the job to the pool
            self.__workq.put((xid, args, kwds))
        else:
            # In on-demand mode: spawn a new thread to do the job
            thr = threading.Thread(target=self._do_process_transaction,
                                   args=(xid,)+args, kwargs=kwds)

            # Register the thread for this transaction
            self.__lock.acquire()
            try:
                self.__workers[xid] = thr
            finally:
                self.__lock.release()

            try:
                thr.start()
            except:
                # Oops, cannot start worker...
                self.__lock.acquire()
                try:
                    del self.__workers[xid]
                finally:
                    self.__lock.release()

                # Sending exception back to sender
                ex = sys.exc_info()[1]
                if ex is not None:
                    ex._trace = traceback.format_exc()
                else:
                    ex = sys.exc_info()[0]
                self._send((xid, ("EXCEPTION", ex)))
                
    def _pool_work(self):
        """Method run by the pool worker threads in pool mode"""
        while 1:
            # Simply consume the jobs from the queue until we get the
            # sentinel token
            data = self.__workq.get()
            if is_sentinel(data):
                break

            xid, args, kwds = data
            # Will raise exception ONLY when connection problems:
            self._do_process_transaction(xid, *args, **kwds)

    def _do_process_transaction(self, xid, *args, **kwds):
        """Method run by the worker threads to process one transaction"""
        # Call process_transaction and prepare the result to send
        result = None
        try:
            result = ("OK", self.process_transaction(*args, **kwds))
        except Exception, ex:
            ex._trace = traceback.format_exc
            result = ("EXCEPTION", ex)
        except:
            ex = sys.exc_info()[1]
            if ex is not None:
                ex._trace = traceback.format_exc()
            else:
                ex = sys.exc_info()[0]
            result = ("EXCEPTION", ex)
        finally:
            if result is None:
                ex = RuntimeError("Unexpected error !")
                result = ("EXCEPTION", ex)

        # Send response
        self._send((xid, result))

        # Unregister the thread in on-demand mode
        if self.__nworkers is None:
            self.__lock.acquire()
            try:
                # In on-demand mode: unregister the thread for this transaction
                del self.__workers[xid]
            finally:
                self.__lock.release()

    def process_transaction(self, *args, **kwds):
        """Implement this method in order to generate a response from
        the given transaction arguments"""
        raise NotImplementedError("Children must implement this method")

    def stop(self):
        """Stop the worker threads and close the channel"""
        ReceiverThread.stop(self)

        #
        # No lock because the listening thread is dead already (no new
        # thread)
        #

        # Clearing job queue
        if self.__workq is not None:
            while 1:
                try:
                    self.__workq.get_nowait()
                except Queue.Empty:
                    break

        # Stopping workers
        if self.__nworkers is not None:
            for i in range(self.__nworkers):
                self.__workq.put(SENTINEL)
            for thr in self.__workers:
                thr.join()
        else:
            while self.__workers:
                xid, thr = self.__workers.popitem()
                thr.join()


class SimpleChannelEndpoint:
    """Construct a channel compliant with the channel specifications
    from a pair of r/w file descriptors"""
    SZI = struct.calcsize('I')
    
    def __init__(self, fd_r, fd_w):
        """
        \param r,w The read-write file descriptors used for this endpoint
        """
        self._fd_r  = fd_r
        self._fd_w  = fd_w
        self._wlock = threading.Lock() # send() has to be thread-safe

    def fileno(self):
        """Return a file descriptor suitable for select/poll of data
        ready to be received in non-blocking mode (at least for the
        first byte)"""
        return self._fd_r

    def send(self, data):
        """send the given python data to the receiving party"""
        sdata = pickle.dumps(data)
        sdata = struct.pack('I', len(sdata)) + sdata
        self._wlock.acquire()
        try:
            os.write(self._fd_w, sdata)
        finally:
            self._wlock.release()

    def recv(self):
        """wait for python data from the sending party and return it"""
        (expected,) = struct.unpack('I', os.read(self._fd_r, self.SZI))
        sdata = ""
        while 1:
            sdata += os.read(self._fd_r, expected - len(sdata))
            assert len(sdata) <= expected
            if len(sdata) == expected:
                break
        return pickle.loads(sdata)

    def close(self):
        """close the endpoint in both send/receive directions"""
        self._wlock.acquire()
        try:
            os.close(self._fd_w)
        finally:
            self._wlock.release()

        os.close(self._fd_r)


def ChannelPair():
    """Very simple function returning a connected pair of channels"""
    r1, w2 = os.pipe()
    r2, w1 = os.pipe()
    return ( SimpleChannelEndpoint(r1, w1), SimpleChannelEndpoint(r2, w2) )


def _test():
    """
    Some tests
    """
    import time, thread

    c1, c2 = ChannelPair()
    mux = Mux(c1)

    class MyDeMux(DeMux):
        """A demultiplexer in which each transaction is a call to sleep()"""
        def process_transaction(self, message_before, duration, message_after):
            """One trasaction is just a call to sleep"""
            print "[%d] BEGIN: %s (sleep %fs)" % (thread.get_ident(),
                                                  message_before, duration)
            time.sleep(duration)
            print "[%d] END: %s" % (thread.get_ident(), message_after)

    class Submitter(threading.Thread):
        """A thread that submits 3 transactions to the mux object"""
        def run(self):
            """Submit 3 transactions and stop"""
            mux.transaction("msg1", 3, "msg2")
            mux.transaction("msg3", 2, "msg4")
            mux.transaction("msg5", 1, "msg6")
            try:
                mux.transaction("msgE", -1, "msgEE")
            except IOError, ex:
                print "Got expected exception from the DeMux: %s" % repr(ex)
 
    demux = MyDeMux(c2, 100)
    # demux = MyDeMux(c2)

    # Starting mux/demux
    mux.start()
    demux.start()

    # Starting as many threads that run transactions as possible
    children = []
    for i in range(700):
        thr = Submitter()
        try:
            thr.start()
            children.append(thr)
        except:
            break

    print "Started %d submission threads" % len(children)

    # Waiting for the children
    for thr in children:
        try:
            thr.join()
        except KeyboardInterrupt:
            print "User interruption."
            break

    # Stopping mux/demux
    mux.stop()
    demux.stop()

    print "Bye."


if __name__ == "__main__":
    _test()
