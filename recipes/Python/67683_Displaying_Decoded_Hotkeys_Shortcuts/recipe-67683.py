PythonWin 2.1 (#15, Jun 18 2001, 21:42:28) [MSC 32 bit (Intel)] on win32.
Portions Copyright 1994-2001 Mark Hammond (MarkH@ActiveState.com) - see 'Help/About PythonWin' for further copyright information.
>>> import sys
>>> # append the complete name of the folder that contains 'link.py'
>>> # (the demo use of pythoncom.CoCreateInstance with shell.CLSID_ShellLink
>>> # in the ActiveState distribution of Python)
>>> # on your computer to sys.path (to make 'link.py' accessible)
>>> #
>>> sys.path.append ( r'C:\Python21\win32comext\shell\test' )
>>> import link
>>> import commctrl
>>> class PyShortcut_II ( link.PyShortcut ):
... 	def decode_hotkey ( self ):
... 		hk = self.GetHotkey ( )
... 		result = ''
... 		if hk: 
... 			mod = hk >> 8
... 			if mod & commctrl.HOTKEYF_SHIFT: result += 'Shift-'
... 			if mod & commctrl.HOTKEYF_CONTROL: result += 'Control-'
... 			if mod & commctrl.HOTKEYF_ALT: result += 'Alt-'
... 			result += chr ( hk % 256 )
... 		return result
... 	
>>> shortcut = PyShortcut_II ( )
>>> shortcut.load ( r'C:\WINDOWS\DESKTOP\Pygris.lnk' )
>>> shortcut.decode_hotkey ( )
'Control-Alt-T'
