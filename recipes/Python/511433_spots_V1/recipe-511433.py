'''Module for Send Python Object Through Socket (SPOTS).

This module implements the Zero SPOTS Protocol, the Query/Reply Protocol,
the Query/Reply Interface, and a shortcut for constructing QRI objects.'''

################################################################################

__version__ = '$Revision: 0 $'
__date__ = 'February 11, 2007'
__author__ = 'Stephen "Zero" Chappell <my.bios@gmail.com>'
__credits__ = '''\
T. Parker, for testing code that led to this module.
B. Brown, for teaching me some math courses.
G. Rossum, for allowing thread support in Python.'''

################################################################################

import base255 as _base255
import cPickle as _cPickle
import sys as _sys
import thread as _thread
import time as _time

################################################################################

class ZSP:

    'ZSP(socket) -> ZSP'

    def __init__(self, socket):
        'Initialize the Zero SPOTS Protocol object.'
        self.__sock = socket
        self.__send = _thread.allocate_lock()
        self.__recv = _thread.allocate_lock()
        self.__temp = ''

    def send(self, obj):
        'Send one object.'
        string = _base255.encode(_cPickle.dumps(obj, _cPickle.HIGHEST_PROTOCOL)) + '\0'
        self.__send.acquire()
        try:
            self.__sock.sendall(string)
        finally:
            self.__send.release()

    def recv(self):
        'Receive one object.'
        self.__recv.acquire()
        try:
            while '\0' not in self.__temp:
                temp = self.__sock.recv(2 ** 12)
                if not temp:
                    if self.__temp:
                        raise IOError
                    else:
                        raise EOFError
                self.__temp += temp
            temp, self.__temp = self.__temp.split('\0', 1)
        finally:
            self.__recv.release()
        return _cPickle.loads(_base255.decode(temp))

################################################################################

class QRP:

    'QRP(ZSP) -> QRP'

    def __init__(self, ZSP):
        'Initialize the Query/Reply Protocol object.'
        self.__ZSP = ZSP
        self.__error = None
        self.__Q_anchor = []
        self.__Q_packet = []
        self.__R_anchor = {}
        self.__Q_lock = _thread.allocate_lock()
        self.__R_lock = _thread.allocate_lock()
        _thread.start_new_thread(self.__thread, ())

    def send_Q(self, ID, obj):
        'Send one query.'
        if self.__error:
            raise self.__error
        self.__ZSP.send((False, ID, obj))

    def recv_Q(self, timeout=None):
        'Receive one query.'
        if self.__error:
            raise self.__error
        if timeout is not None:
            if not isinstance(timeout, (float, int, long)):
                raise TypeError, 'timeout must be of type float, int, or long'
            if not timeout >= 0:
                raise ValueError, 'timeout must be greater than or equal to 0'
        self.__Q_lock.acquire()
        try:
            try:
                if self.__Q_packet:
                    Q = True
                    ID, obj = self.__Q_packet.pop()
                else:
                    Q = False
                    anchor = [_thread.allocate_lock()]
                    anchor[0].acquire()
                    self.__Q_anchor.append(anchor)
            finally:
                self.__Q_lock.release()
        except AttributeError:
            raise self.__error
        if Q:
            return ID, obj
        if timeout:
            _thread.start_new_thread(self.__Q_thread, (timeout, anchor))
        anchor[0].acquire()
        try:
            Q = anchor[1]
        except IndexError:
            if self.__error:
                raise self.__error
            raise Warning
        return Q

    def send_R(self, ID, obj):
        'Send one reply.'
        if self.__error:
            raise self.__error
        self.__ZSP.send((True, ID, obj))

    def recv_R(self, ID, timeout=None):
        'Receive one reply.'
        if self.__error:
            raise self.__error
        if timeout is not None:
            if not isinstance(timeout, (float, int, long)):
                raise TypeError, 'timeout must be of type float, int, or long'
            if not timeout >= 0:
                raise ValueError, 'timeout must be greater than or equal to 0'
        anchor = [_thread.allocate_lock()]
        anchor[0].acquire()
        self.__R_lock.acquire()
        try:
            try:
                self.__R_anchor[ID] = anchor
            finally:
                self.__R_lock.release()
        except AttributeError:
            raise self.__error
        if timeout:
            _thread.start_new_thread(self.__R_thread, (timeout, ID))
        anchor[0].acquire()
        try:
            R = anchor[1]
        except IndexError:
            if self.__error:
                raise self.__error
            raise Warning
        return R

    def __thread(self):
        'Private class method.'
        try:
            while True:
                R, ID, obj = self.__ZSP.recv()
                if R:
                    self.__R_lock.acquire()
                    if self.__R_anchor.has_key(ID):
                        self.__R_anchor[ID].append(obj)
                        self.__R_anchor[ID][0].release()
                        del self.__R_anchor[ID]
                    self.__R_lock.release()
                else:
                    self.__Q_lock.acquire()
                    if self.__Q_anchor:
                        anchor = self.__Q_anchor.pop()
                        anchor.append((ID, obj))
                        anchor[0].release()
                    else:
                        self.__Q_packet.append((ID, obj))
                    self.__Q_lock.release()
        except Exception, error:
            if isinstance(error, EOFError):
                self.__error = EOFError
            else:
                self.__error = IOError
            self.__Q_lock.acquire()
            for anchor in self.__Q_anchor:
                anchor[0].release()
            del self.__Q_anchor
            del self.__Q_packet
            self.__Q_lock.release()
            self.__R_lock.acquire()
            for key in self.__R_anchor:
                self.__R_anchor[key][0].release()
            del self.__R_anchor
            self.__R_lock.release()

    def __Q_thread(self, timeout, anchor):
        'Private class method.'
        _time.sleep(timeout)
        self.__Q_lock.acquire()
        if not self.__error and anchor in self.__Q_anchor:
            anchor[0].release()
            self.__Q_anchor.remove(anchor)
        self.__Q_lock.release()

    def __R_thread(self, timeout, ID):
        'Private class method.'
        _time.sleep(timeout)
        self.__R_lock.acquire()
        if not self.__error and self.__R_anchor.has_key(ID):
            self.__R_anchor[ID][0].release()
            del self.__R_anchor[ID]
        self.__R_lock.release()

################################################################################

class QRI:

    'QRI(QRP) -> QRI'

    def __init__(self, QRP):
        'Initialize the Query/Reply Interface object.'
        self.__QRP = QRP
        self.__ID = 0
        self.__lock = _thread.allocate_lock()

    def call(self, obj, timeout=None):
        'Send one query and receive one reply.'
        self.__lock.acquire()
        ID = ''.join(chr(self.__ID >> shift & 0xFF) for shift in xrange(24, -8, -8))
        self.__ID = (self.__ID + 1) % (2 ** 32)
        self.__lock.release()
        self.__QRP.send_Q(ID, obj)
        return self.__QRP.recv_R(ID, timeout)

    def query(self, timeout=None):
        'Receive one query.'
        return self.__QRP.recv_Q(timeout)

    def reply(self, ID, obj):
        'Send one reply.'
        self.__QRP.send_R(ID, obj)

################################################################################

def qri(socket):
    'Construct a QRI object.'
    return QRI(QRP(ZSP(socket)))

################################################################################

if __name__ == '__main__':
    _sys.stdout.write('Content-Type: text/plain\n\n')
    _sys.stdout.write(file(_sys.argv[0]).read())
