#==============================================================================#
Server.py
#==============================================================================#
import time

class Server:

    def __init__(self, max_age):
        self.__max_age = max_age * 60
        self.__message = {}
        self.__ticket = 1

    def add(self, ID, message):
        self.__message[self.__ticket] = time.clock(), ID, message
        self.__ticket += 1

    def query(self, ID, ticket):
        if not self.__message:
            return 0, []
        minimum = min(self.__message)
        if ticket < minimum:
            ticket = minimum
        messages = []
        for index in range(ticket, self.__ticket):
            clock, message_ID, message = self.__message[index]
            if message_ID != ID:
                messages.append('%s: %s' % (message_ID, message))
        return self.__ticket, messages

    def serve(self):
        while True:
            if not self.__message:
                time.sleep(self.__max_age)
            else:
                time.sleep(self.__max_age + self.__message[min(self.__message)][0] - time.clock())
                del self.__message[min(self.__message)]

import z_service

def main():
    chat_server = Server(5)
    rpc_server = z_service.Sync_Server('', 9000)
    rpc_server.add_service('add', chat_server.add)
    rpc_server.add_service('query', chat_server.query)
    chat_server.serve()

if __name__ == '__main__':
    main()
#==============================================================================#
Input.py
#==============================================================================#
import z_service

def main():
    name = raw_input('Name: ')
    client = z_service.Client(raw_input('Host: '), 9000)
    while True:
        client('add', name, raw_input('Say: '))

if __name__ == '__main__':
    main()
#==============================================================================#
Output.py
#==============================================================================#
import z_service, time

def main():
    name = raw_input('Name: ')
    client = z_service.Client(raw_input('Host: '), 9000)
    ticket = 0
    while True:
        temp_ticket, messages = client('query', name, ticket)
        if temp_ticket:
            ticket = temp_ticket
            for message in messages:
                print message
        time.sleep(5)

if __name__ == '__main__':
    main()
#==============================================================================#
Logger.py
#==============================================================================#
import z_service, time

def main():
    log = file(raw_input('Filename: '), 'w')
    client = z_service.Client(raw_input('Host: '), 9000)
    ticket = 0
    while True:
        temp_ticket, messages = client('query', None, ticket)
        if temp_ticket:
            ticket = temp_ticket
            for message in messages:
                log.write(message + '\n')
        time.sleep(60 * 4)

if __name__ == '__main__':
    main()
