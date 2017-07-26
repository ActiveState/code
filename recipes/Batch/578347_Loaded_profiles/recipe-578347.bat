@echo off
  if "%1" equ "" goto:help
  setlocal enabledelayedexpansion
    set key="HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
    for /f "tokens=2 delims=\" %%i in ('2^>nul reg^
     query HKEY_USERS ^| findstr /v Classes ^| sort') do (
      for %%j in ("-s", "/s") do if "%1" equ "%%~j" echo.%%i
      for %%j in ("-p", "/p") do if "%1" equ "%%~j" (
        if "%%i" equ ".DEFAULT" (
          echo.Default
        ) else (
          for /f "skip=4 tokens=2,* delims=%%" %%k in ('reg^
           query %key%\%%i /v ProfileImagePath') do (
            set "str=%%k%%l"
            if "%%k" equ "systemroot" set "str=!str:systemroot=%systemroot%!"
            if "%%k" equ "SystemDrive" set "str=!str:SystemDrive=%systemdrive%!"
            echo.!str!
          )
        )
      )
    )
  endlocal & goto:eof
  
  :help
  echo.%~n0 v2.01 - shows loaded profiles
  echo.Copyright ^(C^) 2012-2013 - greg zakharov
  echo.ActiveState - code.activestate.com
  echo.
  echo.Usage: %~n0 [/s^|/p]
  echo.   s - print SID of each profile only
  echo.   p - show profile path location
  echo.Note: Default profile is alias of S-1-5-18.
exit /b
