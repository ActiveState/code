@echo off
  setlocal
    if [%1] equ [] goto:help
    (echo %1 | findstr /r /c:[0-9])>nul && if %errorlevel% neq 1 (
      if exist %2 call:head %2 %1
    )
    if exist %1 call:head %1 10
    goto:eof
    
    :head
      for /f "skip=2 tokens=1,* delims=][" %%i in ('find /n /v "" %1') do (
        echo.%%j& if "%%i" equ "%2" goto:eof
      )
  endlocal
exit /b

:help
  echo.%~n0 v1.0 - reads first N strings in text files
  echo.
  echo.Usage: %~n0 [numver] ^<text file name^>
  echo.e.g.: %~n0 events.log   - read first ten strings
  echo.e.g.: %~n0 3 events.log - print only three first strings
exit /b 1
