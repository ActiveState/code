import sys,os
import ctypes
import win32api
import pprint
import win32con
class cscargv:
	def __init__(self,CommandLine=None):
		if CommandLine==None:
			CommandLine=win32api.GetCommandLine()
		argv_count=ctypes.c_int()
		self.cmd_string=ctypes.c_wchar_p(CommandLine)
		CommandLineToArgvW=ctypes.windll.shell32.CommandLineToArgvW
		self.array_memory_address=CommandLineToArgvW(self.cmd_string,ctypes.byref(argv_count))
		match_array_type=ctypes.c_wchar_p*argv_count.value
		self.raw_result=match_array_type.from_address(self.array_memory_address)
		self.result=[arg for arg in self.raw_result]
		self.argv=self.result[:]
	def __str__(self):
		return pprint.pformat(self.result)
	def __repr__(self):
		return repr(self.raw_result)
	def results(self):
		return self.result
	def argvs(self):
		return self.result
	def __del__(self):
		if self.array_memory_address != win32con.NULL:
			retval = ctypes.windll.kernel32.LocalFree(self.array_memory_address)
			if retval != win32con.NULL:
				raise Exception( "LocalFree() failed." )
		else:
			raise Exception( "CommandLineToArgvW() failed." )
if __name__=='__main__':
	c2a=cscargv()
	print c2a
	print repr(c2a)
	print c2a.argv
