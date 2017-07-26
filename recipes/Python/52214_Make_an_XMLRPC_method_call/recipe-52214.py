from xmlrpclib import Server

server = Server("http://www.oreillynet.com/meerkat/xml-rpc/server.php")

print server.meerkat.getItems(
 {'search': '[Pp]ython', 'num_items': 5, 'descriptions': 0}
)
