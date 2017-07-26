import os, proxy, sys, thread

if not os.path.exists('proxy.ini'):
    file('proxy.ini', 'w').write('''\
localhost 80 8080
127.0.0.1 80 9090 <server_name> <server_port> <proxy_port> <optional_text>\
''')

################################################################################

def main(setup, error):
    sys.stderr = file(error, 'a')
    for line in file(setup):
        parts = line.split()
        proxy.Proxy(('', int(parts[2])), (parts[0], int(parts[1]))).start()
    lock = thread.allocate_lock()
    lock.acquire()
    lock.acquire()

################################################################################

if __name__ == '__main__':
    main('proxy.ini', 'error.log')
