import httplib,base64,socket

user='proxy_login';passwd='proxy_pass'
host='login.yahoo.com';port=443
phost='proxy_host';pport=80

#setup basic authentication
user_pass=base64.encodestring(user+':'+passwd)
proxy_authorization='Proxy-authorization: Basic '+user_pass+'\r\n'
proxy_connect='CONNECT %s:%s HTTP/1.0\r\n'%(host,port)
user_agent='User-Agent: python\r\n'
proxy_pieces=proxy_connect+proxy_authorization+user_agent+'\r\n'

#now connect, very simple recv and error checking
proxy=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
proxy.connect((phost,pport))
proxy.sendall(proxy_pieces)
response=proxy.recv(8192) 
status=response.split()[1]
if status!=str(200):  raise 'Error status=',str(status)

#trivial setup for ssl socket
ssl = socket.ssl(proxy, None, None)
sock = httplib.FakeSocket(proxy, ssl)

#initalize httplib and replace with your socket
h=httplib.HTTPConnection('localhost')
h.sock=sock
h.request('GET','/')
r=h.getresponse()
print r.read()
