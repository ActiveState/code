#! /usr/bin/env python

import struct

def getrecord(file,uid, preserve = False):
  """Returns [int(unix_time),string(device),string(host)] from the lastlog formated file object, set preserve = True to preserve your position within the file"""
  position = file.tell()
  recordsize = struct.calcsize('L32s256s')
  file.seek(recordsize*uid)
  data = file.read(recordsize)
  if preserve:
    file.seek(position)
  try:
    returnlist =  list(struct.unpack('L32s256s',data))
    returnlist[1] = returnlist[1].replace('\x00','')
    returnlist[2] = returnlist[2].replace('\x00','')
    return returnlist
  except:
    return False

if __name__ == '__main__':
  import sys
  import pwd
  import time

  try:
    llfile = open("/var/log/lastlog",'r')
  except:
    print "Unable to open /var/log/lastlog"
    sys.exit(1)

  for user in pwd.getpwall():
    record = getrecord(llfile,user[2])
    if record and record[0] > 0:
      print '%16s\t\t%s\t%s' % (user[0],time.ctime(record[0]),record[2])
    elif record:
      print '%16s\t\tNever logged in' % (user[0],)
    else:
      pass
  llfile.close()
