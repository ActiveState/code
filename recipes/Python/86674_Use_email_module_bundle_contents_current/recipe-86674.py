#!/usr/bin/env python

import cStringIO
import base64
import email.Message
import email.Utils
import mimetypes
import os
import quopri

toAddr="example@example.com"
fromAddr="example@example.com"
outputFile="dirContentsMail"

def main():
  mainMsg=email.Message.Message()
  mainMsg["To"]=toAddr
  mainMsg["From"]=fromAddr
  mainMsg["Subject"]="Directory contents"
  mainMsg["Date"]=email.Utils.formatdate(localtime=1)
  mainMsg["Message-ID"]=email.Utils.make_msgid()
  mainMsg["Mime-version"]="1.0"
  mainMsg["Content-type"]="Multipart/mixed"
  mainMsg.preamble="Mime message\n"
  mainMsg.epilogue="" # To ensure that message ends with newline
  
  firstSubMsg=email.Message.Message()
  firstSubMsg["Content-type"]="text/plain"
  firstSubMsg["Content-transfer-encoding"]="7bit"
  firstSubMsg.set_payload("Files from directory\n")
  mainMsg.attach(firstSubMsg)
  
  # Get names of plain files
  fileNames=[f for f in os.listdir(os.curdir) if os.path.isfile(f)]
  for fileName in fileNames:
    contentType,ignored=mimetypes.guess_type(fileName)
    if contentType==None: # If no guess, use generic opaque type
      contentType="application/octet-stream"
    contentsEncoded=cStringIO.StringIO()
    f=open(fileName,"rb")
    mainType=contentType[:contentType.find("/")]
    if mainType=="text":
      cte="quoted-printable"
      quopri.encode(f,contentsEncoded,1) # 1 for encode tabs
    else:
      cte="base64"
      base64.encode(f,contentsEncoded)
    f.close()
    subMsg=email.Message.Message()
    subMsg.add_header("Content-type",contentType,name=fileName)
    subMsg.add_header("Content-transfer-encoding",cte)
    subMsg.set_payload(contentsEncoded.getvalue())
    contentsEncoded.close()
    mainMsg.attach(subMsg)

  f=open(outputFile,"wb")
  f.write(mainMsg.as_string())
  f.close()
  return None

if __name__=="__main__":
  main()
