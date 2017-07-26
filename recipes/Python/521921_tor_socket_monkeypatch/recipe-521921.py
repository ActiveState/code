from construct import *
import socket
import sys
import subprocess
import logging

# monkeys were here
# currently only works with AF_INET and SOCK_STREAM due
# to my shitty understanding of patching getaddrinfo
# but at least it doesn't leak DNS resolves

TORIP="127.0.0.1"
TORPORT=9050
PROTO="socks4a" # or socks5, dependent on tor-resolve
USERID="anonymous" # for 4a only

log = logging.getLogger("torSocket")

class IpAddressAdapter(Adapter):
	def _encode(self, obj, context):
		return "".join(chr(int(b)) for b in obj.split("."))
	def _decode(self, obj, context):
		return ".".join(str(ord(b)) for b in obj)

def IpAddress(name):
	return IpAddressAdapter(Bytes(name, 4))

class SocksException(Exception):
	pass

class TorSocket():
	def __init__(self, *args, **kwargs):
		self._sock = oldSocket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect = getattr(self, "%sconnect" % PROTO)
		self._sock.connect((TORIP, TORPORT))

	def socks5connect(self, address):
		log.debug("using socks5")
		connect = Struct("connect",
				Byte("ver"),
				Byte("nmethods"),
				Byte("methods"),
		)

		connectResponse = Struct("response",
				Byte("ver"),
				Byte("method"),
		)

		p = Container(
				ver=5,
				nmethods=1,
				methods=0
		)

		self._sock.send(connect.build(p))
		data = self._sock.recv(1024)

		response = connectResponse.parse(data)
		if response.method == 255:
			raise SocksException

		request = Struct("request",
				Byte("ver"),
				Byte("cmd"),
				Byte("rsv"),
				Byte("atyp"),
				IpAddress("dstaddr"),
				UBInt16("dstport")
		)

		requestResponse = Struct("requestResponse",
				Byte("ver"),
				Byte("rep"),
				Byte("rsv"),
				Byte("atyp"),
				UBInt16("bndport")
		)

		p = Container(
				ver=5,
				cmd=1,
				rsv=0,
				atyp=1,
				dstaddr=address[0],
				dstport=address[1]
		)

		self._sock.send(request.build(p))

		data = self._sock.recv(1024)
		response = requestResponse.parse(data)

		if response.rep != 0:
			raise SocksException

	def socks4aconnect(self, address):
		log.debug("using socks4a")

		connect = Struct("connect",
				Byte("ver"),
				Byte("cd"),
				UBInt16("dstport"),
				IpAddress("dstip"),
				CString("userid"),
				CString("domain")
		)

		connectResponse = Struct("response",
				Byte("ver"),
				Byte("cd"),
				UBInt16("dstport"),
				IpAddress("dstip")
		)

		p = Container(
				ver=4,
				cd=1,
				dstport=address[1],
				dstip="0.0.0.1",
				userid=USERID,
				domain=address[0]
		)

		self._sock.send(connect.build(p))
		data = self._sock.recv(1024)

		response = connectResponse.parse(data)
		if response.cd != 90:
			raise SocksException

	def connect(self, address):
		raise NotImplementedError

	def makefile(self, *args):
		return self._sock.makefile(*args)

	def sendall(self, *args):
		self._sock.sendall(*args)

	def send(self, *args):
		self._sock.send(*args)

	def recv(self, *args):
		return self._sock.recv(*args)

	def close(self):
		self._sock.close()

def torResolve(name):
	log.debug("resolving %s with tor-resolve" % name)
	p = subprocess.Popen(['tor-resolve', name], stdout=subprocess.PIPE)
	ip = p.stdout.read().strip()
	return ip

def getaddrinfo(*args):
	if PROTO == "socks4a":
		return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
	elif PROTO == "socks5":
		ip = torResolve(args[0])
		return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, args[1]))]
	else:
		raise SocksException

oldSocket = socket.socket
oldAddrInfo = socket.getaddrinfo

socket.socket = TorSocket
socket.getaddrinfo = getaddrinfo
socket.gethostbyname = torResolve
sys.modules['socket'] = socket
