# SendMAPIMail Module.

# Authoir:  P. Young
# Date:     Sep, 2002

import win32com.client.dynamic, sys, re

def SetReceipients(Message,Recipients,RecipientType):

   for recipient in re.split('\;',Recipients):
      recip = Message.Recipients.Add(Name=recipient, Type=RecipientType)
      recip.Resolve()

def SendMAPIMail(MAPIProfile=None, SendTo=None, SendCC=None, SendBCC=None, Subject=None, Message=None):
   # Create a mapi session
   mapi = win32com.client.dynamic.Dispatch("MAPI.session")
   if MAPIProfile <> None:
      mapi.Logon(MAPIProfile)
   else:
      mapi.Logon("MS Exchange Settings")

   # Create a new message
   if Subject == None: Subject = ''
   if Message == None: Message = ''
   outbox = mapi.OutBox.Messages.Add(Subject,Message,'CMC: IPM')

   # Set the recipients
   SetReceipients(outbox,SendTo,1)
   if SendCC <> None: SetReceipients(outbox,SendCC,2)
   if SendBCC <> None: SetReceipients(outbox,SendBCC,3)

   # Update and send the message
   outbox.Update()
   outbox.Send()
   mapi.DeliverNow()

   # terminate the MAPI session and kill the objects   
   mapi.Logoff()
   outbox = None
   mapi = None

if __name__ == '__main__':
   MAPIProfile = None
   SendTo = None
   SendCC = None
   SendBCC = None
   SendSubject = None
   SendMessage = None
    
   if len(sys.argv) == 1:       # token not found
      print "Syntax:"
      print "SendSMTPMail.py -p <MAPI Profile> -t <Send to> -c <CC to> -b <BCC to> -s <subject> -m <message>"
      sys.exit(-1)
     
   i=1
   while i < len(sys.argv):
      if sys.argv[i] == '-p':
         i = i+1
         MAPIProfile = sys.argv[i]
         i = i+1
         continue
      if sys.argv[i] == '-t':
         i = i+1
         SendTo = sys.argv[i]
         i = i+1
         continue
      if sys.argv[i] == '-c':
         i = i+1
         SendCC = sys.argv[i]
         i = i+1
         continue
      if sys.argv[i] == '-b':
         i = i+1
         SendBCC = sys.argv[i]
         i = i+1
         continue
      if sys.argv[i] == '-s':
         i = i+1
         SendSubject = sys.argv[i]
         i = i+1
         continue
      if sys.argv[i] == '-m':
         i = i+1
         SendMessage = sys.argv[i]
         i = i+1
         continue
     # token not found

      print "Syntax:"
      print "SendSMTPMail.py -p <MAPI Profile> -t <Send to> -c <CC to> -b <BCC to> -s <subject> -m <message>"
      sys.exit(-1)

   SendMAPIMail(MAPIProfile, SendTo, SendCC, SendBCC, SendSubject, SendMessage)   
