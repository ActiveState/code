import socket, string

#some user data, change as per your taste
SERVER = '2night.azzurra.org'
PORT = 6667
NICKNAME = 'test_py'
CHANNEL = '#test_py'

#open a socket to handle the connection
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#open a connection with the server
def irc_conn():
    IRC.connect((SERVER, PORT))

#simple function to send data through the socket
def send_data(command):
    IRC.send(command + '\n')

#join the channel
def join(channel):
    send_data("JOIN %s" % channel)

#send login data (customizable)
def login(nickname, username='user', password = None, realname='Pythonist', hostname='Helena', servername='Server'):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)

irc_conn()
login(NICKNAME)
join(CHANNEL)

while (1):
    buffer = IRC.recv(1024)
    msg = string.split(buffer)
    if msg[0] == "PING": #check if server have sent ping command
        send_data("PONG %s" % msg[1]) #answer with pong as per RFC 1459
    if msg [1] == 'PRIVMSG' and msg[2] == NICKNAME:
        filetxt = open('/tmp/msg.txt', 'a+') #open an arbitrary file to store the messages
        nick_name = msg[0][:string.find(msg[0],"!")] #if a private message is sent to you catch it
        message = ' '.join(msg[3:])
        filetxt.write(string.lstrip(nick_name, ':') + ' -> ' + string.lstrip(message, ':') + '\n') #write to the file
        filetxt.flush() #don't wait for next message, write it now!
