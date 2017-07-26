RegObj.dll is an ActiveX server--and, hence, has an automation interface--that is available with documentation in 
the distribution file known as RegObji.exe, from the following page:

    http://msdn.microsoft.com/vbasic/downloads/addins.asp
    
To provide early binding for RegObj use 

 >>> from win32com.client import gencache
 >>> gencache.EnsureModule('{DE10C540-810E-11CF-BBE7-444553540000}', 0, 1, 0)
 
or the MakePy utility within PythonWin, referring to "Regstration Manipulation Classes (1.0)" (Please notice
the spelling error.)
 
Sample use, to determine what command is associated with a Python file:

>>> from win32com.client import Dispatch, gencache
>>> from win32con import HKEY_CLASSES_ROOT

>>> gencache.EnsureModule('{DE10C540-810E-11CF-BBE7-444553540000}', 0, 1, 0)

>>> regobj = Dispatch ( 'RegObj.Registry' )

>>> HKCR = regobj.RegKeyFromHKey ( HKEY_CLASSES_ROOT )

>>> PythonFileKey = HKCR.ParseKeyName('Python.File\Shell\Open\command')
>>> PythonFileKey.Value
u'J:\\Python22\\pythonw.exe "%1" %*'
