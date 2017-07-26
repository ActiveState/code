import socket
import BaseHTTPServer

class Server(BaseHTTPServer.HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        # 10 second timeout
        self.socket.settimeout(10.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
            except socket.timeout:
                pass
        # Reset timeout on the new socket
        result[0].settimeout(None)
        return result

if __name__ == '__main__':
    from SimpleHTTPServer import SimpleHTTPRequestHandler

    server = Server(('', 80), SimpleHTTPRequestHandler)
    server.serve_forever()
