import _winreg
x=_winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
y= _winreg.OpenKey(x,
 r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
print "Your environment variables are"
print "#","name","value","type"
for i in range(1000):
    try:
        n,v,t=_winreg.EnumValue(y,i)
        print i,n,v,t
    except EnvironmentError:
        print "You have",i,"Environment variables"
        break
print "Your PATH was "    
path = _winreg.QueryValueEx(y,"path")[0]
print path
_winreg.CloseKey(y)
# Reopen Environment key for writing.
y=_winreg.OpenKey(x,
 r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
 0,_winreg.KEY_ALL_ACCESS)
# now append C:\ to the path
_winreg.SetValueEx(y,"path",0,_winreg.REG_EXPAND_SZ,path+";C:\\")
_winreg.CloseKey(y)
_winreg.CloseKey(x)
