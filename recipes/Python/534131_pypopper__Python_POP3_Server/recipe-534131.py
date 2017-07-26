"""pypopper: a file-based pop3 server

Useage:
    python pypopper.py <port> <path_to_message_file>
"""
import logging
import os
import socket
import sys
import traceback

logging.basicConfig(format="%(name)s %(levelname)s - %(message)s")
log = logging.getLogger("pypopper")
log.setLevel(logging.INFO)

class ChatterboxConnection(object):
    END = "\r\n"
    def __init__(self, conn):
        self.conn = conn
    def __getattr__(self, name):
        return getattr(self.conn, name)
    def sendall(self, data, END=END):
        if len(data) < 50:
            log.debug("send: %r", data)
        else:
            log.debug("send: %r...", data[:50])
        data += END
        self.conn.sendall(data)
    def recvall(self, END=END):
        data = []
        while True:
            chunk = self.conn.recv(4096)
            if END in chunk:
                data.append(chunk[:chunk.index(END)])
                break
            data.append(chunk)
            if len(data) > 1:
                pair = data[-2] + data[-1]
                if END in pair:
                    data[-2] = pair[:pair.index(END)]
                    data.pop()
                    break
        log.debug("recv: %r", "".join(data))
        return "".join(data)


class Message(object):
    def __init__(self, filename):
        msg = open(filename, "r")
        try:
            self.data = data = msg.read()
            self.size = len(data)
            self.top, bot = data.split("\r\n\r\n", 1)
            self.bot = bot.split("\r\n")
        finally:
            msg.close()


def handleUser(data, msg):
    return "+OK user accepted"

def handlePass(data, msg):
    return "+OK pass accepted"

def handleStat(data, msg):
    return "+OK 1 %i" % msg.size

def handleList(data, msg):
    return "+OK 1 messages (%i octets)\r\n1 %i\r\n." % (msg.size, msg.size)

def handleTop(data, msg):
    cmd, num, lines = data.split()
    assert num == "1", "unknown message number: %s" % num
    lines = int(lines)
    text = msg.top + "\r\n\r\n" + "\r\n".join(msg.bot[:lines])
    return "+OK top of message follows\r\n%s\r\n." % text

def handleRetr(data, msg):
    log.info("message sent")
    return "+OK %i octets\r\n%s\r\n." % (msg.size, msg.data)

def handleDele(data, msg):
    return "+OK message 1 deleted"

def handleNoop(data, msg):
    return "+OK"

def handleQuit(data, msg):
    return "+OK pypopper POP3 server signing off"

dispatch = dict(
    USER=handleUser,
    PASS=handlePass,
    STAT=handleStat,
    LIST=handleList,
    TOP=handleTop,
    RETR=handleRetr,
    DELE=handleDele,
    NOOP=handleNoop,
    QUIT=handleQuit,
)

def serve(host, port, filename):
    assert os.path.exists(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    try:
        if host:
            hostname = host
        else:
            hostname = "localhost"
        log.info("pypopper POP3 serving '%s' on %s:%s", filename, hostname, port)
        while True:
            sock.listen(1)
            conn, addr = sock.accept()
            log.debug('Connected by %s', addr)
            try:
                msg = Message(filename)
                conn = ChatterboxConnection(conn)
                conn.sendall("+OK pypopper file-based pop3 server ready")
                while True:
                    data = conn.recvall()
                    command = data.split(None, 1)[0]
                    try:
                        cmd = dispatch[command]
                    except KeyError:
                        conn.sendall("-ERR unknown command")
                    else:
                        conn.sendall(cmd(data, msg))
                        if cmd is handleQuit:
                            break
            finally:
                conn.close()
                msg = None
    except (SystemExit, KeyboardInterrupt):
        log.info("pypopper stopped")
    except Exception, ex:
        log.critical("fatal error", exc_info=ex)
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: [<host>:]<port> <path_to_message_file>"
    else:
        _, port, filename = sys.argv
        if ":" in port:
            host = port[:port.index(":")]
            port = port[port.index(":") + 1:]
        else:
            host = ""
        try:
            port = int(port)
        except Exception:
            print "Unknown port:", port
        else:
            if os.path.exists(filename):
                serve(host, port, filename)
            else:
                print "File not found:", filename
