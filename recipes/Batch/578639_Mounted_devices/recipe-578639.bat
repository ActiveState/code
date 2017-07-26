@echo off
  setlocal enabledelayedexpansion
    ::script info
    set "slf=%~n0 v1.0"
    echo %slf% - mounted devices
    echo Copyright (C) 2013 greg zakharov gregzakh@gmail.com
    echo Activestate - code.activestate.com
    echo.
    ::
    set "i=0"
    set "key=HKLM\SYSTEM\MountedDevices"
    ::searching \DosDevices\
    for /f "tokens=1,3" %%i in ('reg query %key%^
      ^| findstr /r /c:DosDevices ^| sort') do (
        set "arr.!i!=%%i=%%j" & set /a "i+=1"
      )
    )
    ::real length of array
    set /a "len=%i% - 1"
    ::reset increment and create new pair Drive=>Volume
    set "i=0"
    for /l %%i in (0, 1, !len!) do (
      for /f "tokens=1,2 delims==" %%j in ("!arr.%%i!") do (
        ::%%j - device and %%k - data
        for /f "tokens=1,3" %%l in ('reg query %key%^
          ^| findstr /r /c:Volume') do (
          ::%%l - value and %%m - data
          if "%%k" equ "%%m" set "a.!i!=%%j=%%l" & set /a "i+=1"
        )
      )
    )
    ::user friendly output
    for /l %%i in (0, 1, !len!) do (
      for /f "tokens=2* delims=\=" %%j in ("!a.%%i!") do (
        for /f "tokens=2 delims=:" %%l in ('2^>nul dir %%j^
          ^| findstr /i /r [a-z0-9]-[a-z0-9]') do (
          echo Volume: \%%k\
          echo    Mounted at: %%j\
          echo     Volume ID:%%l
        )
        echo.
      )
    )
  endlocal
exit /b
