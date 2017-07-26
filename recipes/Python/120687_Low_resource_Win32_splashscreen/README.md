###Low resource Win32 splashscreen

Originally published: 2002-04-14 15:18:03
Last updated: 2002-04-14 15:18:03
Author: Henk Punt

The following code implements a splash screen as typically found in windows applications. Using only API's available from win32gui, win32api and win32con, it avoids dependancy on MFC (wrapped by win32ui). This way the 600kb or so win32ui.pyd extension DLL is not needed when freezing your app with py2exe.\nAnother 80kb could be squeezed out by not using win32con but to define the necessary constants directly in the code itself.