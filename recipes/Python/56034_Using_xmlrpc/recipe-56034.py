from xmlrpclib import Server
from pprint import pprint

query = {'search':'Python', 'time_period':'7DAYS',}
meerkatURI = 'http://www.oreillynet.com/meerkat/xml-rpc/server.php'

meerkatSrv = Server(meerkatURI)
data = meerkatSrv.meerkat.getItems(query)
pprint(data)
