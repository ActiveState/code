## Execute remote commands on windows like psexecOriginally published: 2011-11-11 13:00:06 
Last updated: 2011-11-18 11:54:42 
Author: Ofer Helman 
 
This code attempts to implement psexec in python code, using wmi.\nAs part of a project of mine I had to run remote commands on remote Windows machines from other Windows machine. At first I used psexec for that with subprocess.Popen.\nThe reason in this code for creating .bat files and running them remotely is because complicated commands do not run properly with Win32_Process.Create\n\nIn this code I used this code: http://code.activestate.com/recipes/442521/history/3/\n\nrequired installations:\n\npywin32 - http://sourceforge.net/projects/pywin32/files/pywin32/Build216/\n\nwmi - http://timgolden.me.uk/python/downloads/