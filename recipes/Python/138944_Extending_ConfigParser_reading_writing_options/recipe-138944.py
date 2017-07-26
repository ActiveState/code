#!L:\Python21\python.exe
"""This module provide classes for manipulation with Config files and 
   other configuration storages

   Classes:
     RegConfigParser - makes ConfigParser able to keep configuration data
	it Windows registry so it works on MS Windows 9x/NT/2000/XP platforms only


	Uses:
		Then I was trying to write first of my Windows services with Python
	  I haven't found the way to set default program directory so 
	  I just wrote these classes that provides ConfigParser interface to the
	  Registry keys

	Limitations:
		I am using HKEY_LOCAL_MACHINE as root key for all operations
	  for all of my applications it's OK. But suggestions appreciated

	Best regards,
      Ivan V. Begtin

	This code published under Python License, see http://www.python.org 
   for details
"""


from ConfigParser import *

try:
	from _winreg import *
except ImportError:
	print "Looks like this OS doesn't support _winreg module."

__version__ = "0.1"
__author__ = "Ivan V. Begtin (erellon@narod.ru)"
__date__ = "$ 11 July 2002 $";

class RegConfigParser(ConfigParser):
	"""Extended ConfigParser that supports reading config from registry"""
	def __init__(self):
		ConfigParser.__init__(self)	

	def readRegKey(self, keyname):
		"""Reads configuration data from registry key"""
		kkey = OpenKey(HKEY_LOCAL_MACHINE, keyname)
		kinfo = QueryInfoKey(kkey)
		for x in range(0, kinfo[0]):
			try:
				subname = EnumKey(kkey, x)
				# Adding this section
				self.add_section(subname)
				# Reading options from it
				subkey = OpenKey(HKEY_LOCAL_MACHINE, keyname + "\\" + subname)
				subkinfo = QueryInfoKey(subkey)
				for x in range(0, subkinfo[1]):
					try:
						(name, value, ttype) = EnumValue(subkey, x)
						self.set(subname, name, value)
					except EnvironmentError:
						break
				subkey.Close()
			except EnvironmentError:
				break		
		# Setting defaults
		for x in range(0, kinfo[1]):
			try:
				(name, value, ttype) = EnumValue(kkey, x)
				self.set("DEFAULT", name, value)
			except EnvironmentError:
				break
		# Close key
		kkey.Close()



	def writeRegKey(self, keyname):
		"""Writes configuration data to the registry key"""
		kkey = CreateKey(HKEY_LOCAL_MACHINE, keyname)		
		kkey.Close()
		kkey = OpenKey(HKEY_LOCAL_MACHINE, keyname, 0, KEY_ALL_ACCESS)	
		# Clean out default values and keys
		kinfo = QueryInfoKey(kkey)
		for x in range(0, kinfo[1]):
			try:
				(name, value, ttype) = EnumValue(kkey, x)
				DeleteValue(kkey, name)
			except EnvironmentError:
				break
		for x in range(0, kinfo[0]):
			try:
				subname = EnumKey(kkey, x)
				DeleteKey(kkey, subname)
			except EnvironmentError:
				break

		# Writing defaults
		defaults = self.defaults()
		for defname in defaults.keys():
			SetValueEx(kkey, defname, 0, REG_SZ, defaults[defname])

		# Creating keys with options
		sections = self.sections()
		for sect in sections:
			subname = keyname + "\\" + sect
			sub_key = CreateKey(HKEY_LOCAL_MACHINE, subname)
			sub_key.Close()
			sub_key = OpenKey(HKEY_LOCAL_MACHINE, subname, 0, KEY_SET_VALUE)
			opts = self.options(sect)
			for opt in opts:
				SetValueEx(sub_key, opt, 0, REG_SZ, self.get(sect, opt))
			sub_key.Close()

		kkey.Close()
		pass


if __name__ == "__main__":
	cfg = RegConfigParser()
	cfg.readRegKey("Software\\AVS Emu")
	cfg.writeRegKey("Software\\AVS")
	cfg.write(open("test.cfg", "w+"))
