#IN THE NAME OF ALLAH
#Nike Name: Pcrlth0n
#(C) 2008
#a simple way to create and change your registry on windows


import win32api
def new_key():
    reg1 = open('C:\\reg1.reg', 'w')
    reg1.write("""REGEDIT4\n[HKEY_CURRENT_USER\\Example""")
    reg1.close()
    win32api.WinExec('reg import C:\\reg1.reg', 0)
def new_string_key():
    reg2 = open('C:\\reg2.reg', 'w')
    reg2.write("""REGEDIT4\n[HKEY_CURRENT_USER\\Example]\n"String Key"="C:\\\\\"""")
    reg2.close()
    win32api.WinExec('reg import C:\\reg2.reg', 0)
def new_dword_key():
    reg3 = open('C:\\reg3.reg', 'w')
    reg3.write("""REGEDIT4\n[HKEY_CURRENT_USER\\Example]\n"Dword key"=dword:00000000 """)
    reg3.close()
    win32api.WinExec('reg import C:\\reg3.reg', 0)

#new_key()
#new_string_key()
#new_dword_key()
