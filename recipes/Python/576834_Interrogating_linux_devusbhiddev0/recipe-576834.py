#!/usr/bin/python
import struct, array, fcntl

class struxx:
  _fields = None
  _format = None
  _buffer = None
  def __init__(self):
    self.reset()

  def __len__(self):
    """binary represntation length, for fields, use __dict__ or something"""
    return struct.calcsize(self._format)

  def __iter__(self):
    return [getattr(self, field) for field in self._fields.split(";")].__iter__()

  def reset(self):
    for field in self._fields.split(";"):
      setattr(self, field, 0)
    self._buffer = array.array('B', [0]*len(self))

  def pack(self):
    self._buffer = array.array('B', struct.pack(self._format, *self))

  def unpack(self):
    rv = struct.unpack(self._format, self._buffer)
    for i in range(len(rv)):
      setattr(self, self._fields.split(";")[i], rv[i])

  def ioctl(self, fd, ioctlno):
    self.pack()
    rv = fcntl.ioctl(fd, ioctlno, self._buffer, True)
    self.unpack()
    return rv

class uint(struxx):
  _fields = "uint"
  _format = "I"
  def get_version(self, fd): return self.ioctl(fd, HIDIOCGVERSION)
  def get_flags(self, fd): return self.ioctl(fd, HIDIOCGFLAG)
  def set_flags(self, fd): return self.ioctl(fd, HIDIOCSFLAG)

class hiddev_devinfo(struxx):
  _fields = "bustype;busnum;devnum;ifnum;vendor;product;version;num_applications"
  _format = "IIIIhhhI"
  def get(self, fd): return self.ioctl(fd, HIDIOCGDEVINFO)

class hiddev_string_descriptor(struxx):
  _fields = "index;value"
  _format = "i256c"

  def reset(self):
    self.index = 0
    self.value = '\0'*256

  def pack(self):
    tmp = struct.pack("i", self.index) + self.value[:256].ljust(256, '\0')
    self._buffer = array.array('B', tmp)

  def unpack(self):
    self.index = struct.unpack("i", self._buffer[:4])
    self.value = self._buffer[4:].tostring()

  def get_string(self, fd, idx):
    self.index = idx
    return self.ioctl(fd, HIDIOCGSTRING)

class hiddev_report_info(struxx):
  _fields = "report_type;report_id;num_fields"
  _format = "III"
  def get_info(self, fd): return self.ioctl(fd, HIDIOCGREPORTINFO)

class hiddev_field_info(struxx):
  _fields = "report_type;report_id;field_index;maxusage;flags;physical;logical;application;logical_minimum;logical_maximum;physical_minimum;physical_maximum;unit_exponent;unit"
  _format = "I"*8+"i"*4+"II"
  def get_info(self, fd): return self.ioctl(fd, HIDIOCGFIELDINFO)

class hiddev_usage_ref(struxx):
  _fields = "report_type;report_id;field_index;usage_index;usage_code;value"
  _format = "I"*5+"i"

class hiddev_collection_info(struxx):
  _fields = "index;type;usage;level"
  _format = "I"*4
  def get_info(self, fd, index):
    self.index = index
    return self.ioctl(fd, HIDIOCGCOLLECTIONINFO)

class hiddev_event(struxx):
  _fields = "hid;value"
  _format = "Hi"

IOCPARM_MASK = 0x7f
IOC_NONE = 0x20000000
IOC_WRITE = 0x40000000
IOC_READ = 0x80000000

def FIX(x): return struct.unpack("i", struct.pack("I", x))[0]

def _IO(x,y): return FIX(IOC_NONE|(ord(x)<<8)|y)
def _IOR(x,y,t): return FIX(IOC_READ|((t&IOCPARM_MASK)<<16)|(ord(x)<<8)|y)
def _IOW(x,y,t): return FIX(IOC_WRITE|((t&IOCPARM_MASK)<<16)|(ord(x)<<8)|y)
def _IOWR(x,y,t): return FIX(IOC_READ|IOC_WRITE|((t&IOCPARM_MASK)<<16)|(ord(x)<<8)|y)

HIDIOCGVERSION         =_IOR('H', 0x01, struct.calcsize("I"))
HIDIOCAPPLICATION      =_IO('H', 0x02)
HIDIOCGDEVINFO         =_IOR('H', 0x03, len(hiddev_devinfo()))
HIDIOCGSTRING          =_IOR('H', 0x04, len(hiddev_string_descriptor()))
HIDIOCINITREPORT       =_IO('H', 0x05)
def HIDIOCGNAME(buflen): return _IOR('H', 0x06, buflen)
HIDIOCGREPORT          =_IOW('H', 0x07, len(hiddev_report_info()))
HIDIOCSREPORT          =_IOW('H', 0x08, len(hiddev_report_info()))
HIDIOCGREPORTINFO      =_IOWR('H', 0x09, len(hiddev_report_info()))
HIDIOCGFIELDINFO       =_IOWR('H', 0x0A, len(hiddev_field_info()))
HIDIOCGUSAGE           =_IOWR('H', 0x0B, len(hiddev_usage_ref()))
HIDIOCSUSAGE           =_IOW('H', 0x0C, len(hiddev_usage_ref()))
HIDIOCGUCODE           =_IOWR('H', 0x0D, len(hiddev_usage_ref()))
HIDIOCGFLAG            =_IOR('H', 0x0E, struct.calcsize("I"))
HIDIOCSFLAG            =_IOW('H', 0x0F, struct.calcsize("I"))
HIDIOCGCOLLECTIONINDEX =_IOW('H', 0x10, len(hiddev_usage_ref()))
HIDIOCGCOLLECTIONINFO  =_IOWR('H', 0x11, len(hiddev_collection_info()))
def HIDIOCGPHYS(buflen): return _IOR('H', 0x12, buflen)

HID_REPORT_TYPE_INPUT   =1
HID_REPORT_TYPE_OUTPUT  =2
HID_REPORT_TYPE_FEATURE =3
HID_REPORT_TYPE_MIN     =1
HID_REPORT_TYPE_MAX     =3
HID_REPORT_ID_UNKNOWN =0xffffffff
HID_REPORT_ID_FIRST   =0x00000100
HID_REPORT_ID_NEXT    =0x00000200
HID_REPORT_ID_MASK    =0x000000ff
HID_REPORT_ID_MAX     =0x000000ff

def enum_reports(fd):
  for report_type in (HID_REPORT_TYPE_INPUT,
                      HID_REPORT_TYPE_OUTPUT,
                      HID_REPORT_TYPE_FEATURE):
    for i in range(HID_REPORT_ID_MAX+1):
      try:
        ri = hiddev_report_info()
        ri.report_type = report_type
        ri.report_id = i
        #print "trying", ri.__dict__
        ri.get_info(fd)
        print "%s(%s): %s fields" % ({1: 'input', 2:'output', 3:'feature'}.get(ri.report_type), ri.report_id, ri.num_fields)
        for field in range(ri.num_fields):
          fi = hiddev_field_info()
          fi.report_type = ri.report_type
          fi.report_id = ri.report_id
          fi.field_index = field
          fi.get_info(fd)
          print ", ".join(["%s:%s" % (key, fi.__dict__[key]) for key in fi.__dict__ if key not in ("report_type", "report_id", "_buffer") and fi.__dict__[key] ])
        #print report_info.__dict__
        print
      except IOError:
        pass


if __name__=="__main__":
#  name = ""
#  for name in globals():
#    if name.startswith("HID"):
#      if type(globals()[name]) == int:
#        print name, "\t%x" % globals()[name]

  f = open("/dev/usb/hiddev0", "r")
  tmp = uint()
  tmp.get_version(f)
  print "version 0x%x" % tmp.uint
  tmp.get_flags(f)
  print "flags 0x%x" % tmp.uint
  tmp.uint = 3
  tmp.set_flags(f)
  tmp.get_flags(f)
  print "flags 0x%x" % tmp.uint


  devinfo = hiddev_devinfo()
  devinfo.get(f)
  print "devinfo", devinfo.__dict__

  enum_reports(f)

def get_device_name(f):
  a = array.array('B', [0]*1024)
  fcntl.ioctl(f, HIDIOCGNAME(1024), a, True)
  print a

def get_some_strings(f):
  for i in range(-10000, 10000):
    try:
      string = hiddev_string_descriptor()
      string.get_string(f, i)
      print "string %s: %s", string.index, repr(string.value)
    except IOError:
      pass


def show_all_collections(f):
  for i in range(256):
    try:
      collection_info = hiddev_collection_info()
      collection_info.get_info(f, i)
      print "coll %s" % i, collection_info.__dict__
      print """
idnex: %(index)s
type:  %(type)s
level: %(level)s
usage: 0x%(usage)x""" % collection_info.__dict__
    except IOError:
      pass
