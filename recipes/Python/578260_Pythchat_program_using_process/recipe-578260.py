#!/usr/bin/env python
# Added by <ctang@redhat.com>
import sys
import os
from multiprocessing import connection


ADDR = ('', 9997)
AUTH_KEY = '12345'

class Server(object):

    def __init__(self, username):
        self.auth_key = AUTH_KEY
        self.addr = ADDR
        self.username = username
        self.listener = connection.Listener(self.addr, authkey=self.auth_key)

    def listen(self):
        while True:
            conn = self.listener.accept()
            while True:
                try:
                    request = conn.recv()
                    response = self.response(request)
                    conn.send(response)
                except EOFError:
                    break
            conn.close()

    def reply(self):
        message = raw_input("%s: " % self.username)
        return message

    def output_request(self, request):
        sys.stdout.write('%s says: %s\n' % request)

    def response(self, request):
        self.output_request(request)
        response = (self.username, self.reply())
        return response

class Client(object):

    def __init__(self, username):
        self.auth_key = AUTH_KEY
        self.addr = ADDR
        self.username = username
        self.display_name = self.make_display_name(username)

    def make_display_name(self, username):
        return "%s: " % username

    def connect(self):
        self.conn = connection.Client(self.addr, authkey=self.auth_key)
        while True:
            message = raw_input(self.display_name)
            self.send(message)
            response = self.conn.recv()
            self.output_response(response) 

    def send(self, message):
        self.conn.send((self.username, message))

    def output_response(self, response):
        sys.stdout.write('%s says: %s\n' % response)

def main():
    mode = sys.argv[1]
    if mode == 'server':
        username = raw_input("Your name please: ")
        server = Server(username)
        server.listen()
    elif mode == 'client':
        username = raw_input("Your name please: ")
        client = Client(username)
        client.connect()

if __name__ == '__main__':
    main()
