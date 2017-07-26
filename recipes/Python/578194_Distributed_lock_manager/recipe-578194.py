#!/usr/bin/env python    
# -*- coding: utf-8 -*-
                   
import logging            
import os            
import select            
import socket            
import sys      
import thread
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Lock(object):
    def __init__(self, client, name):
        self.name = name
        self.client = client

    def __enter__(self):
        self.acquire()
        return self
  
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
 
    def acquire(self):
        self.client.communicate('acquire %s' % self.name)
    
    def release(self):
        self.client.communicate('release %s' % self.name)        
        

class LockClient(object):
    buffer_size = 128
    
    def __init__(self, host, port, name):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self.name = name
   
    def mkLock(self, name):
        self.communicate('mklock %s' %  name)
        return Lock(self, name)

    def mkRLock(self, name):
        self.communicate('mkrlock %s' % name)
        return Lock(self, name)
  
    def reset(self):
        self.communicate('reset x')  

    def communicate(self, data):
        self._socket.send('%s %s' % (self.name, data))
        self._socket.recv(self.buffer_size)
      
    def close(self):
        try:
            self._socket.close()
        except socket.error:
            pass


class LockServer(threading.Thread):
    buffer_size = 128
    locks = {}
    
    def __init__(self, _socket, address):
        super(LockServer, self).__init__()
        
        self.protocol = {
            'mklock': self.mkLock,
            'mkrlock': self.mkRLock,
            'acquire': self.acquire,
            'release': self.release,
            'reset': self.reset
        }
        
        self._socket = _socket
        self.setDaemon(True)
        self.start()

    def run(self):
        try:
            self.run_server()
        except (EOFError, ValueError, socket.error), e:
            logger.error(e)

        try:
            self._socket.close()
        except socket.error:
            pass

    def run_server(self):
        while True:
            data = self._socket.recv(self.buffer_size)
            
            if data in ('', '\n', '\r\n'):
                return
            
            try:
                who, op, name = data.split()
            except ValueError:
                raise ValueError('Invalid data')
            
            try:
                fn = self.protocol[op]
            except KeyError:
                raise ValueError('%s: invalid operation "%s"' % (who, op))
            
            fn(who, name)
            
            self._socket.send(data)

    def get_lock(self, who, name):
        try:
            return LockServer.locks[name]
        except KeyError:
            raise ValueError('%s: unknown lock "%s"' % (who, name))
        
    def acquire(self, who, name):
        self.get_lock(who, name).acquire(True)
        
        logger.info('%s acquired %s', who, name)
   
    def release(self, who, name):
        try:
            self.get_lock(who, name).release()
        except thread.error, e:
            raise ValueError('%s: cannot unlock %s: %s' % (who, name, e))
        
        logger.info('%s released %s', who, name)

    def reset(self, who, name):
        LockServer.locks = {}
        
        logger.warning('%s reseted all locks', who, name)

    def mkLock(self, who, name, lock=threading.Lock):
        if name not in LockServer.locks:
            LockServer.locks[name] = lock()
            
            logger.info('%s created %s', who, name)
        else:
            logger.info('%s uses %s', who, name)
            
    def mkRLock(self, who, name):
        return self.mklock(who, name, lock=threading.RLock)


def serve_forever():
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        host, port = ( os.environ.get('DLM') or sys.argv[1] ).split(':')
        port = int(port)
    except (IndexError, ValueError):
        host, port = 'localhost', 27272
    
    try:
        _socket.bind((host, port))
        _socket.listen(5)

        logger.info('Listening on %s:%s', host, port )

        while True:
            inputs =  [ _socket ]
            inputready, outputready, exceptready = select.select(inputs, [], [])

            [ LockServer(*stream.accept()) for stream in inputready ]
    finally:
        try:
            _socket.close()
            logger.info('Socket closed')
        except socket.error:
            pass

if __name__ == '__main__':
    serve_forever()
