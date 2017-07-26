@echo off
  setlocal
    if "%1" equ "/fix:me" (
      call:fix
      echo.::not_indexed>>"%~dpnx0"
      goto:eof
    )
    for /f "tokens=* delims=:" %%i in ('findstr "^::" "%~dpnx0"') do (
      if "%%i" equ "not_indexed" (
        call:fix
        for /f "tokens=*" %%i in ('mountvol ^| findstr /r \:\\$') do (
          (2>nul dir %%i /s /b & 2>nul dir /a:h /s /b)>>"%~dpnx0"
        )
      )
    )
    if "%1" neq "" (
      for /f "tokens=*" %%i in ('findstr /i /r /c:%1 "%~dpnx0"') do (
        if exist "%%i" echo %%i
      )
    )
    goto:eof
  :fix
    for /f "tokens=* delims=" %%i in ('mountvol^
     ^| findstr /v /b /i /r /c:[a-z]:\\ /c::: "%~dpnx0"') do (
      echo.%%i>>source.tmp
    )
    move /y source.tmp "%~dpnx0"
  endlocal
exit /b
::not_indexed
