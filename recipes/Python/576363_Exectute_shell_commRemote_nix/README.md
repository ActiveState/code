## Exectute shell command on Remote *nix machine

Originally published: 2008-07-18 02:20:22
Last updated: 2008-07-18 02:20:22
Author: winterTTr Dong

Use telnetlib to execute the shell command from localhost.\n\nAn example to show the funciton.\nOutput the result to result.log.\n\nfrom PyRemoteControl import RemoteShellCommand\n\n# host info\nhost_ip = '192.168.32.72'\nuser_name = 'fw'\npassword = 'fw'\nresult_file = 'result.log'\n\n# command List\ncmdList = [ 'cd' , 'll' ]\n\n# init\ncursor = RemoteShellCommand( host_ip , user_name , password , result_file )\ncursor.AddPrompt(  '\\[fw@localhost .*\\]\\$ ')\ncursor.AddPrompt(  '\\[root@localhost .*\\]# ' )\n\n# connect to Linux\ncursor.Login()\n\n# change to root\ncursor.SendInterActiveCmd( 'su - ' , [ ('Password: ' , 'rootPassord')]  , False)\n\n# Exec Command\nfor cmd in cmdList :\n    cursor.SendCmd( cmd )\n\n# logout\ncursor.Logout()