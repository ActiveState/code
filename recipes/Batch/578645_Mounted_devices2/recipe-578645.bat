@echo off
  setlocal
    set "s=%~n0 v1.01"
    echo %s% - mounted devices
    echo Copyright (C) 2013 greg zakharov gregzakh@gmail.com
    echo.
    ::volumes and drives
    for /f "tokens=* delims= " %%i in ('mountvol ^| findstr \\') do (
      if "%%~di\" neq "%%i" (echo Volume: %%i) else (echo    Mounted at: %%i)
      ::ids
      for /f "tokens=2 delims=:" %%j in ('2^>nul vol %%~di') do (
        echo    Volume ID:%%j
        echo.
      )
    )
  endlocal
exit /b
