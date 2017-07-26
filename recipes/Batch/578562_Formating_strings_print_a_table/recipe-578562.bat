@echo off
 setlocal enabledelayedexpansion
  for /l %%i in (1, 1, 9) do (
    for /l %%j in (1, 1, 9) do (
      set /a "res=%%i * %%j"
      rem This condition imitate "\t" character
      if "!res:~1,2!" equ "" (set "res= !res!,") else set "res=!res!,"
      rem Imitation of C's print function
      <nul set /p "res=   !res:,= !"
    )
    echo.
  )
 endlocal
exit /b
