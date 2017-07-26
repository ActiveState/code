import ctypes

def work_area():
  class RECT(ctypes.Structure):
     _fields_ = [('left',ctypes.c_ulong),
                 ('top',ctypes.c_ulong),
                 ('right',ctypes.c_ulong),
                 ('bottom',ctypes.c_ulong)]
  r = RECT()
  ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_GETWORKAREA, 0, ctypes.byref(r), 0)
  return map(int, (r.left, r.top, r.right, r.bottom))

print work_area()
