# ----------------------------------------------------------------------------------------------------
#  Python / Skype4Py example that prints out chat messages
#
#  Tested with  Skype4Py version 0.9.28.5 and Skype verson 3.8.0.96

import sys
import os
import time
import Skype4Py
import random

def ndsSay(ndsWords):
    ndsIn = str(ndsWords)
    zcmd='espeak "'+ndsIn+'"'
    print zcmd
    f=os.popen(zcmd)
    f.close()
    ndsWords=""
    ndsTalk=""
    zcmd=''
        
# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in
#case.
def OnAttach(status):
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

    if status == Skype4Py.apiAttachSuccess:
       print('***************************************')


# ----------------------------------------------------------------------------------------------------
# Fired on chat message status change. 
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'        

def OnMessageStatus(Message, Status):
    if Status == 'RECEIVED':
        print(Message.FromDisplayName + ': ' + Message.Body)
        ndsSay(Message.FromDisplayName)
        ndsSay(Message.Body)

    if Status == 'READ':
        ndsMonkey = "todo"
        print(Message.FromDisplayName + ': ' + Message.Body)
        ndsSay(Message.FromDisplayName)
        ndsSay(Message.Body)

    if Status == 'SENT':
        print('Myself ' + Message.Body)


# ----------------------------------------------------------------------------------------------------
# Creating instance of Skype object, assigning handler functions and attaching to Skype.
skype = Skype4Py.Skype()
skype.OnAttachmentStatus = OnAttach
skype.OnMessageStatus = OnMessageStatus

print('***************************************')
print 'Connecting to Skype..'
skype.Attach()

# ----------------------------------------------------------------------------------------------------
# Looping until user types 'exit'
Cmd = ''
while not Cmd == 'exit':
    Cmd = raw_input('')
