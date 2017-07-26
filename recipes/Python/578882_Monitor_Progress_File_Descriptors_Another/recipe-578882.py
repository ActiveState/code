#!/usr/bin/env python
#
# fdprogress.py -- by Alfe (alfe@alfe.de), inspired by azat@Stackoverflow
#
# usage:  fdprogress.py <pid>
#

import time, os, os.path

from collections import defaultdict

def getFds(pid):
  return os.listdir('/proc/%s/fd/' % pid)

def getPos(pid, fd):
  with open('/proc/%s/fdinfo/%s' % (pid, fd)) as f:
    return int(f.readline()[5:])

def getSize(pid, fd):
  return os.path.getsize(getPath(pid, fd))

class FdIsPipe(Exception): pass

def getPath(pid, fd):
  result = os.readlink('/proc/%s/fd/%s' % (pid, fd))
  if result.startswith('pipe:['):
    raise FdIsPipe(result)
  return result

def extendHistory(history, pid):
  for fd in getFds(pid):
    try:
      history[fd, getPath(pid, fd)].append(
        (time.time(), getPos(pid, fd), getSize(pid, fd)))
    except FdIsPipe:
      pass  # ignore fds to pipe

def initHistory(pid):
  result = defaultdict(list)
  extendHistory(result, pid)
  return result

def reduceHistory(history):
  for key, value in history.iteritems():
    if len(value) > 2:
      del value[1:-2]  # only keep first and last
      # (this can be more clever in the future)

def entryPrediction(fd, path, values):
  t1, pos1, size1 = values[0]
  t2, pos2, size2 = values[-1]
  if t1 == t2:  # no time passed yet?
    return fd, path, (t2, pos2, size2), None, None, None, None, None, None, None
  growth = (size2 - size1) / (t2 - t1)  # bytes/sec growth of file
  if growth != 0:
    tSize0 = t1 - size1 / growth  # time when size was 0
  else:
    tSize0 = None
  speed = (pos2 - pos1) / (t2 - t1)  # speed of pos in bytes/sec
  if speed != 0:
    tPos0 = t1 - pos1 / speed  # time when pos was 0
    tPosSize2 = t1 + (size2 - pos1) / speed  # time of pos reaching size2
  else:
    tPos0 = tPosSize2 = None
  if speed != growth:  # when will both meet?
    tm = t2 + (size2 - pos2) / (speed - growth)
    sizeM = size2 + growth * (tm - t2)
  else:
    tm = sizeM = None
  return (fd, path, (t2, pos2, size2), growth, speed, tSize0, tPos0,
          tPosSize2, tm, sizeM)

def eachPrediction(history):
  for (fd, path), values in history.iteritems():
    yield entryPrediction(fd, path, values)

def displayTime(t):
  if t is None:
    return "<>"
  d = t - time.time()
  try:
    lt = time.localtime(t)
  except:
    return "??"
  return (
    time.strftime("%%F (now%+dy)" % (d/86400/365), lt)
    if abs(d) > 2 * 86400 * 365 else
    time.strftime("%%F (now%+dM)" % (d/86400/30), lt)
    if abs(d) > 2 * 86400 * 30 else
    time.strftime("%%F (now%+dd)" % (d/86400), lt)
    if abs(d) > 2 * 86400 else
    time.strftime("%%a, %%T (now%+dh)" % (d/3600), lt)
    if time.strftime('%F', lt) != time.strftime('%F', time.localtime()) else
    time.strftime("%%T (now%+dh)" % (d/3600), lt)
    if abs(d) > 2 * 3600 else
    time.strftime("%%T (now%+dm)" % (d/60), lt)
    if abs(d) > 2 * 60 else
    time.strftime("%%T (now%+ds)" % d, lt))

def displaySize(size):
  return (
    "<>" if size is None else
    "%d B" % size
    if size < 1e3 else
    "%.2f kB" % (size / 1e3)
    if size < 1e6 else
    "%.2f MB" % (size / 1e6)
    if size < 1e9 else
    "%.2f GB" % (size / 1e9))

def displaySpeed(speed):
  return displaySize(speed) + "/s"

def printPrediction(history):
  for (fd, path, (t2, pos2, size2), growth, speed, tSize0, tPos0,
       tPosSize2, tm, sizeM) in eachPrediction(history):
    print '\n', fd, "->", os.path.basename(path)
    dT = displayTime
    dSi = displaySize
    dSp = displaySpeed
    print "size:", dSi(size2), "\tgrowth:", dSp(growth), \
          "\t\tpos:", dSi(pos2), "\tspeed:", dSp(speed)
    print "emptyTime:", dT(tSize0), "\tstartTime:", dT(tPos0), \
          "\treachTime:", dT(tPosSize2), "\tmeetTime:", dT(tm)

def main(argv):
  pid = argv[1]
  history = initHistory(pid)
  while True:
    os.system('clear')
    printPrediction(history)
    extendHistory(history, pid)
    reduceHistory(history)
    time.sleep(1.0)

if __name__ == '__main__':
  import sys
  sys.exit(main(sys.argv))
