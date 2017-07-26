def write(_socket, data):
    f = _socket.makefile('wb', buffer_size )
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    f.close()

def read(_socket):
    f = _socket.makefile('rb', buffer_size )
    data = pickle.load(f)
    f.close()
    return data
