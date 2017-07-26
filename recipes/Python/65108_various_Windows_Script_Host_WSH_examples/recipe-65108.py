import sys
import win32api
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
# launch Notepad to edit this script, simple version
# sys.argv[0] is WScript.ScriptFullName in WSH
#shell.Run("notepad " + sys.argv[0])

# this time set the window type, wait for Notepad to be shut down by the user,
# and save the error code returned from Notepad when it is shut down
# before proceeding
ret = shell.Run("notepad " + sys.argv[0], 1, 1)
print ret

# open a command window, change to the path to C:\ ,
# and execute the DIR command
shell.Run("cmd /K CD C:\ & Dir")

# environment strings
print shell.ExpandEnvironmentStrings("%windir%")
