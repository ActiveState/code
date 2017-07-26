import socket
import sys
import thread

def main(setup, error):
    sys.stderr = file(error, 'a')
    for settings in parse(setup):
        thread.start_new_thread(server, settings)
    lock = thread.allocate_lock()
    lock.acquire()
    lock.acquire()

def parse(setup):
    settings = list()
    for line in file(setup):
        parts = line.split()
        settings.append((parts[0], int(parts[1]), int(parts[2])))
    return settings

def server(*settings):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind(('', settings[2]))
        dock_socket.listen(5)
        while True:
            client_socket = dock_socket.accept()[0]
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((settings[0], settings[1]))
            thread.start_new_thread(forward, (client_socket, server_socket))
            thread.start_new_thread(forward, (server_socket, client_socket))
    finally:
        thread.start_new_thread(server, settings)

def forward(source, destination):
    string = ' '
    while string:
        string = source.recv(1024)
        if string:
            destination.sendall(string)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

if __name__ == '__main__':
    main('proxy.ini', 'error.log')
