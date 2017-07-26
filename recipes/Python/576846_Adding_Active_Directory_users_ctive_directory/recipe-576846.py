this script adds multi users to one group in active directory using python, there is alot of complicated modules which lets python talk to AD using LDAP, but why the hell when we have dsquery and dsmod
so this is a merge of python and AD command line 
please feel free to use it


#
# Author: Mohamed Garrana 
# Creation Date: 26 may'09
#
#
# Description: Adding AD users to a group importing the users from a txt file,where they are written in userlogon name per line
#for example:
#amohsen
#mibrahim
#jsmith
# some lines with # are used for troubleshooting you can comment them out for further diagnostics
########################################################################################
import os
#opening the file users.txt and reading it line by line while stripping the line 
fo = open('users.txt','r')
for line in fo:
name= line.strip()
#using the AD command dsmod piped with dsquery 
command = 'dsquery user -samid %s | dsmod group "CN for the group, for example CN=group1;DN=microsoft;DN=com" -addmbr' %(name,)
nr=os.popen(command)
# readd=nr.read() 
