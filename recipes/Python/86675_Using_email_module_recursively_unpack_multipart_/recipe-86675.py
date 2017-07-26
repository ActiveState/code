#!/usr/bin/env python

import email.Message
import email.Parser
import os
import sys

# This is the hard way for illustration. In practice,
# msg.walk() is simpler.
def writePartsRecurse(msg):
  global partCounter
  # Message/RFC822 parts are bundled this way
  while isinstance(msg.get_payload(),email.Message.Message):
    msg=msg.get_payload()

  if msg.is_multipart():
    for subMsg in msg.get_payload():
       writePartsRecurse(subMsg)
  else:
    name=msg.get_param("name")
    if name==None:
      name="part-%i" % partCounter
    partCounter+=1
    # In real life, make sure that name is a reasonable
    # filename on your OS.
    f=open(name,"wb")
    f.write(msg.get_payload(decode=1))
    f.close()
    print name
  return None

def main():
  global partCounter

  if len(sys.argv)==1:
    print "Usage: %s filename" % os.path.basename(sys.argv[0])
    sys.exit(1)

  mailFile=open(sys.argv[1],"rb")
  p=email.Parser.Parser()
  msg=p.parse(mailFile)
  mailFile.close()

  partCounter=1
  writePartsRecurse(msg)
  return None


if __name__=="__main__":
  main()
