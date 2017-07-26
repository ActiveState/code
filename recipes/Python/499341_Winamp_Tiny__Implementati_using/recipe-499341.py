#======================================================================
# 
# winamp.py - winamp control interface
# copyright 2006 (c) skywind3000@hotmail.com
#
# NOTE: 
#
# This module is a tiny winamp implementation using ctypes, which
# presents mp3/wav/mid/ogg... playback in python by calling winamp
# plugins. Treating it as a little example for advanced ctypes usage
#
# most of common plugins in winamp5 or above need a shared dll named 
# nscrt.dll, you need copy it to current dir from %winamp%/plugins/
#
# the plugins in winamp4.0/2.0 do not need it, you can only copy 
# in_*.dll or out_*.dll to current dir 
#
# for more information, please see http://www.winamp.com/nsdn/winamp/
# to get full example (in_mp3.dll, out_wave.dll, sample.mp3 include): 
# http://www.joynb.net/blog/up/1166948100.rar
#
#======================================================================

import sys, os, time
import ctypes
from ctypes import c_long, c_char_p, c_voidp, c_int, c_short, c_byte
from ctypes import POINTER, CFUNCTYPE, pointer, byref
from ctypes import cast, addressof, cdll, windll
from ctypes.wintypes import *


#----------------------------------------------------------------------
# struct OutModule definition
#----------------------------------------------------------------------
class OutModule(ctypes.Structure):
    _fields_ = [
		("version", c_long), 
		("description", c_char_p),
		("id", c_int),
		("hMainWindow", c_voidp),
		("hDllInstance", c_voidp),
		("config", CFUNCTYPE(None, c_voidp)),
		("about", CFUNCTYPE(None, c_voidp)),
		("init", CFUNCTYPE(None,)),
		("quit", CFUNCTYPE(None,)),
		("open", CFUNCTYPE(c_int, c_int, c_int, c_int, c_int, c_int)),
		("close", CFUNCTYPE(None,)),
		("write", CFUNCTYPE(c_int, c_voidp, c_int)),
		("canwrite", CFUNCTYPE(c_int,)),
		("isplaying", CFUNCTYPE(c_int,)),
		("pause", CFUNCTYPE(c_int, c_int)),
		("setvol", CFUNCTYPE(None, c_int)),
		("setpan", CFUNCTYPE(None, c_int)),
		("flush", CFUNCTYPE(None, c_int)),
		("getoutputtime", CFUNCTYPE(c_int,)),
		("getwrittentime", CFUNCTYPE(c_int,))
	]


#----------------------------------------------------------------------
# struct InModule definition
#----------------------------------------------------------------------
class InModule(ctypes.Structure):
    _fields_ = [
		("version", c_long), 
		("description", c_char_p),
		("hMainWindow", c_voidp),
		("hDllInstance", c_long),
		("FileExtensions", c_char_p),
		("is_seekable", c_int),
		("UsesOutputPlug", c_int),
		("config", CFUNCTYPE(None, c_voidp)),	# 7
		("about", CFUNCTYPE(None, c_voidp)),
		("init", CFUNCTYPE(None,)),
		("quit", CFUNCTYPE(None,)),
		("getfileinfo", CFUNCTYPE(None, c_char_p, c_char_p, POINTER(c_int))),
		("infobox", CFUNCTYPE(c_int, c_char_p, c_voidp)),
		("isourfile", CFUNCTYPE(c_int, c_char_p)),
		("play", CFUNCTYPE(c_int, c_char_p)), # 14
		("pause", CFUNCTYPE(None, )),
		("unpause", CFUNCTYPE(None, )),
		("ispaused", CFUNCTYPE(c_int, )),
		("stop", CFUNCTYPE(None, )),
		("getlength", CFUNCTYPE(c_int, )),
		("getoutputtime", CFUNCTYPE(c_int, )),
		("setoutputtime", CFUNCTYPE(None, c_int)),
		("setvol", CFUNCTYPE(None, c_int)),
		("setpan", CFUNCTYPE(None, c_int)), # 23
		("SAVSAInit", CFUNCTYPE(None, c_int, c_int)),
		("SAVSADeInit", CFUNCTYPE(None, )),
		("SAAddPCMData", CFUNCTYPE(None, c_voidp, c_int, c_int, c_int)),
		("SAGetMode", CFUNCTYPE(c_int,)),
		("SAAdd", CFUNCTYPE(None, c_voidp, c_int, c_int)),
		("VSAAddPCMData", CFUNCTYPE(None, c_voidp, c_int, c_int, c_int)),
		("VSAGetMode", CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))),
		("VSAAdd", CFUNCTYPE(None, c_voidp, c_int)),
		("VSASetInfo", CFUNCTYPE(None, c_int, c_int)),
		("dsp_isactive", CFUNCTYPE(c_int, )),
		("dsp_dosamples", CFUNCTYPE(c_int, c_voidp, c_int, c_int, c_int, c_int)),
		("eqset", CFUNCTYPE(None, c_int, c_char_p, c_int)),
		("setinfo", CFUNCTYPE(None, c_int, c_int, c_int, c_int)),
		("outmod", POINTER(OutModule))
	]


# export OutModule from dll
def load_outmod(dllname):
	outdll = ctypes.cdll.LoadLibrary(dllname)
	getaddr = outdll.winampGetOutModule
	getaddr.restype = c_voidp
	# outmod = (OutModule*)(getaddr())
	outmod = cast(getaddr(), POINTER(OutModule))[0]
	return outmod

# export InModule from dll
def load_inmod(dllname):
	indll = ctypes.cdll.LoadLibrary(dllname)
	getaddr = indll.winampGetInModule2
	getaddr.restype = c_voidp
	# inmod = (InModule*)(getaddr())
	inmod = cast(getaddr(), POINTER(InModule))[0]
	return inmod

# init inmod/outmod together
def init_modules(inmod, outmod):
	def _SAVSAInit(n1, n2): pass
	def _SAVSADeInit(): pass
	def _SAAddPCMData(n1, n2, n3, n4): pass
	def _SAGetMode(): return 0;
	def _SAAdd(n1, n2, n3): pass
	def _VSAAdd(n1, n2): pass
	def _VSAAddPCMData(n1, n2, n3, n4): pass
	def _VSAGetMode(n1, n2): return 0
	def _VSASetInfo(n1, n2): pass
	def _dspisactive(): return 0
	def _dspyesactive(): return 1
	def _dspdo(n1, n2, n3, n4, n5): return 0
	def _setinfo(n1, n2, n3, n4): pass
	def _eqset(n1, n2, n3): pass

	# setting up default dummy functions
	inmod.SAVSAInit = CFUNCTYPE(None, c_int, c_int)(_SAVSAInit)
	inmod.SAVSADeInit = CFUNCTYPE(None, )(_SAVSADeInit)
	inmod.SAAddPCMData = CFUNCTYPE(None, c_voidp, c_int, c_int, c_int)(_SAAddPCMData)
	inmod.SAGetMode = CFUNCTYPE(c_int,)(_SAGetMode)
	inmod.SAAdd = CFUNCTYPE(None, c_voidp, c_int, c_int)(_SAAdd)
	inmod.VSAAdd = CFUNCTYPE(None, c_voidp, c_int)(_VSAAdd)
	inmod.VSAAddPCMData = CFUNCTYPE(None, c_voidp, c_int, c_int, c_int)(_VSAAddPCMData)
	inmod.VSAGetMode = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))(_VSAGetMode)
	inmod.VSASetInfo = CFUNCTYPE(None, c_int, c_int)(_VSASetInfo)
	inmod.dsp_isactive = CFUNCTYPE(c_int, )(_dspisactive)
	inmod.dsp_dosamples = CFUNCTYPE(c_int, c_voidp, c_int, c_int, c_int, c_int)(_dspdo)
	inmod.setinfo = CFUNCTYPE(None, c_int, c_int, c_int, c_int)(_setinfo)
	inmod.eqset = CFUNCTYPE(None, c_int, c_char_p, c_int)(_eqset)

	# setting up other members
	inmod.outmod = pointer(outmod)
	GetActiveWindow = windll.user32.GetActiveWindow
	inmod.hMainWindow = GetActiveWindow()
	inmod.hDllInstance = 0
	outmod.hMainWindow = GetActiveWindow()
	outmod.hDllInstance = 0

	return  0	


#----------------------------------------------------------------------
# Global Variables
#----------------------------------------------------------------------
__in_module = None
__out_module = None

#----------------------------------------------------------------------
# Winamp Main Interface
#----------------------------------------------------------------------
def init(indll, outdll):
	global __in_module, __out_module
	quit()
	try:
		__in_module	= load_inmod(indll)
		__out_module = load_outmod(outdll)
	except: return -1
	init_modules(__in_module, __out_module)
	__out_module.init()
	__in_module.init()
	return 0

def quit():
	global __in_module, __out_module
	if __in_module: 
		__in_module.stop()
		__in_module.quit()
	if __out_module: __out_module.quit()
	__in_module = None
	__out_module = None

def play(name):
	return __in_module.play(name)

def stop():
	__in_module.stop()

def pause(status = True):
	if status: __in_module.pause()
	else: __in_module.unpause()

def ispaused():
	return __in_module.ispaused()

def getlength():
	return __in_module.getlength()

def gettime():
	return __in_module.getoutputtime()

def settime(timems):
	__in_module.setoutputtime(timems)

def setvol(vol = 1.0):
	__in_module.setvolume(int(vol * 255))

def setpan(pan = 0.0):
	__in_module.setpan(int(pan * 127))

def fileinfo(name):
	i = ctypes.c_int()
	s = ctypes.create_string_buffer('\000' * 256)
	__in_module.getfileinfo(name, s, pointer(i))
	return (s.value, i.value)


#----------------------------------------------------------------------
# Testing Code
#----------------------------------------------------------------------
if __name__ == '__main__':
	indll = 'in_mp3.dll'
	outdll = 'out_wave.dll'
	if init(indll, outdll):
		print 'cannot load plugins'
		sys.exit(0)
	name = 'sample.mp3'
	info = fileinfo(name)

	def ms2time(ms):
		if ms <= 0: return '00:00:000'
		time_sec, ms = ms / 1000, ms % 1000
		time_min, time_sec = time_sec / 60, time_sec % 60
		time_hor, time_min = time_min / 60, time_min % 60
		if time_hor == 0: return '%02d:%02d:%03d'%(time_min, time_sec, ms)
		return '%02d:%02d:%02d:%03d'%(time_hor, time_min, time_sec, ms)

	print 'Playing "%s" (%s), press \'q\' to exit ....'%(info[0], name)
	play(name)
	user32 = ctypes.windll.user32
	while 1:
		user32.GetAsyncKeyState.restype = WORD
		user32.GetAsyncKeyState.argtypes = [ ctypes.c_char ]
		if user32.GetAsyncKeyState('Q'): break
		time.sleep(0.1)
		print '[%s / %s]\r'%(ms2time(gettime()), ms2time(getlength())),
		if (gettime() > 0) and (gettime() > getlength() - 3000):
			settime(0)
	print '\nstopped'
	quit()
