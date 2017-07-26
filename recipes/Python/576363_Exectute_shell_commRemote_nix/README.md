## Exectute shell command on Remote *nix machine  
Originally published: 2008-07-18 02:20:22  
Last updated: 2008-07-18 02:20:22  
Author: winterTTr Dong  
  
Use telnetlib to execute the shell command from localhost.

An example to show the funciton.
Output the result to result.log.

from PyRemoteControl import RemoteShellCommand

# host info
host_ip = '192.168.32.72'
user_name = 'fw'
password = 'fw'
result_file = 'result.log'

# command List
cmdList = [ 'cd' , 'll' ]

# init
cursor = RemoteShellCommand( host_ip , user_name , password , result_file )
cursor.AddPrompt(  '\[fw@localhost .*\]\$ ')
cursor.AddPrompt(  '\[root@localhost .*\]# ' )

# connect to Linux
cursor.Login()

# change to root
cursor.SendInterActiveCmd( 'su - ' , [ ('Password: ' , 'rootPassord')]  , False)

# Exec Command
for cmd in cmdList :
    cursor.SendCmd( cmd )

# logout
cursor.Logout()