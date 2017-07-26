import ctypes
user = ctypes.windll.user32

class RECT(ctypes.Structure):
  _fields_ = [
    ('left', ctypes.c_ulong),
    ('top', ctypes.c_ulong),
    ('right', ctypes.c_ulong),
    ('bottom', ctypes.c_ulong)
    ]
  def dump(self):
    return map(int, (self.left, self.top, self.right, self.bottom))

class MONITORINFO(ctypes.Structure):
  _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('rcMonitor', RECT),
    ('rcWork', RECT),
    ('dwFlags', ctypes.c_ulong)
    ]

def get_monitors():
  retval = []
  CBFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
  def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
    r = lprcMonitor.contents
    #print "cb: %s %s %s %s %s %s %s %s" % (hMonitor, type(hMonitor), hdcMonitor, type(hdcMonitor), lprcMonitor, type(lprcMonitor), dwData, type(dwData))
    data = [hMonitor]
    data.append(r.dump())
    retval.append(data)
    return 1
  cbfunc = CBFUNC(cb)
  temp = user.EnumDisplayMonitors(0, 0, cbfunc, 0)
  #print temp
  return retval

def monitor_areas():
  retval = []
  monitors = get_monitors()
  for hMonitor, extents in monitors:
    data = [hMonitor]
    mi = MONITORINFO()
    mi.cbSize = ctypes.sizeof(MONITORINFO)
    mi.rcMonitor = RECT()
    mi.rcWork = RECT()
    res = user.GetMonitorInfoA(hMonitor, ctypes.byref(mi))
    data.append(mi.rcMonitor.dump())
    data.append(mi.rcWork.dump())
    retval.append(data)
  return retval

print monitor_areas()
