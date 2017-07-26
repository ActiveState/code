@echo off
  setlocal
    if [%1] equ [] goto:help
    (echo %1 | findstr /r /c:[0-9])>nul && if %errorlevel% neq 1 (
      if exist %2 call:tail %2 %1
    )    
    if exist %1 call:tail %1 10    
    goto:eof
    
    :tail
      for /f "tokens=*" %%i in ("%~1") do (
        for /f "tokens=3 delims=:" %%j in ('find /c /v "" "%%~fni"') do (
          set /a "str=%%j - %2"
        )
      )
      more +%str% %1
  endlocal
exit /b

:help
  echo.%~n0 v1.01 - reads last N strings in text files
  echo.
  echo.Usage: %~n0 [number] ^<text file name^>
  echo.e.g.: %~n0 events.log   - show last ten strings
  echo.e.g.: %~n0 3 events.log - print only three last strings
exit /b 1
