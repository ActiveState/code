import win32api
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
shell.Run("calc")
win32api.Sleep(100)
shell.AppActivate("Calculator")
win32api.Sleep(100)
shell.SendKeys("1{+}")
win32api.Sleep(500)
shell.SendKeys("2")
win32api.Sleep(500)
shell.SendKeys("~") # ~ is the same as {ENTER}
win32api.Sleep(500)
shell.SendKeys("*3")
win32api.Sleep(500)
shell.SendKeys("~")
win32api.Sleep(2500)
