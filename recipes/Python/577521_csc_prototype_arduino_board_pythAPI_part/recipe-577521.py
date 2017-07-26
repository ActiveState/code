#! /usr/bin/env python
#coding=utf-8

#Author: Cheeng Shu Chin

import serial, time
import traceback
import inspect
import threading

class autoprop(type):
	def __init__(cls, name, bases, dict):
		super(autoprop, cls).__init__(name, bases, dict)
	def __new__(cls,name, bases, dict):
		sf=super(autoprop, cls).__new__(cls,name, bases, dict)
		for key in dict.keys():
			if not (len(key)>5 and key.startswith("_")):
				continue
			nm=key[:5].lower()
			if nm in ["_get_","_set_","_del_"]:
				fget = getattr(sf, "_get_%s" % key[5:], None)
				fset = getattr(sf, "_set_%s" % key[5:], None)
				fdel = getattr(sf, "_del_%s" % key[5:], None)
				setattr(sf,key[5:],property(fget, fset, fdel))
		return sf
	def __getattribute__(self,name):
		return super(autoprop, self).__getattribute__(name)
class arduino(object):
	__metaclass__ = autoprop
	def __init__(self, port, baudrate=115200):
		self._port=port
		self._baudrate=baudrate
		self._serial = None
		self._debug=0
		self._lock=threading.RLock()
		self.nop
	def _get_lock(self):
		self._lock.acquire()
	def _get_unlock(self):
		self._lock.release()
	def _set_debug(self,data):
		self._debug=data
		self('debug','%s'%data)
	def _get_serial(self):
		if self._serial==None:
			self._serial = serial.Serial(self._port, self._baudrate)
		return self._serial
	def close(self):
		self.nop
		self.serial.close()
		return True
	def _get_nop(self):
		self.write="nop"
		self.read
	def swrite(self,data):
		self.lock
		self.serial.write(data)
		self.unlock
	def sread(self):
		self.lock
		dt=self.serial.readline()
		self.unlock
		return dt
	def _set_write(self,data):
		dt=""
		while not dt:
			while not dt.endswith("?"):
				dt+=self.read
			if dt in ["!INT0 ?","!INT1 ?"]:
				getattr(self,dt[1:5].lower())
				dt=""
		if self._debug:
			print dt
		self.swrite(data)
		if self._debug:
			print data
	def _get_int0(self):
		print "INT0",chr(7)
	def _get_int1(self):
		print "INT1",chr(7)
	def _get_read(self):
		return self.sread().strip()
	def _get_frame(self):
		frame=inspect.currentframe().f_back.f_back
		return frame
	def _get_farg(self):
		args, varargs, varkw, largs=inspect.getargvalues(self.frame)
		if args:
			for arg in args[1:]:
				self.write=largs[arg]
		if varargs:
			for arg in varargs:
				self.write=largs[arg]
		return self.read
	def _get_func(self):
		code=self.frame.f_code
		self.write=code.co_name
		return code
	def __call__(self,func,*args):
		self.write=func
		if args:
			for arg in args:
				self.write=arg
		return self.read
class cscarduino(arduino,object):
	__metaclass__ = autoprop
	def __init__(self,*arg):
		arduino.__init__(self,*arg)
	def echo(self,data):
		self.func
		return self.farg
	def pinMode(self,pin, mode):
		self.func
		return self.farg
	def digitalWrite(self,pin,value):
		self.func
		return self.farg
	def analogRead(self,pin):
		self.func
		return self.farg
	def analogWrite(self,pin,value):
		self.func
		return self.farg
if __name__=="__main__":
	cscadn=cscarduino(5)
	cscadn.debug=0
	try:
		cscadn.pinMode("13","1")
		cscadn.pinMode("9","1")
		r=[0,2,4,5,7,9,11,13,15]
		for x in range(len(r)):
			#cscadn("test","0")
			print cscadn.echo(time.asctime())
			cscadn.digitalWrite("13","1")
			#time.sleep(0.1)
			#cscadn.digitalWrite("13","0")
			#time.sleep(1)
			tmp=[]
			for y in range(6):
				tmp.append(cscadn.analogRead('%s'%y))
			print tmp
			#cscadn('pycall','analogWrite',"9","%s"%r[x])
			cscadn.analogWrite("9","%s0"%r[x])
			cscadn.digitalWrite("13","0")
			#cscadn("test","1")
	except:
		print "Error!"
		print traceback.format_exc()
	finally:
		#cscadn.write="!"
		cscadn.close()
