@echo off
  setlocal
    ::condition for execution
    if "%1" leq "0" (
      echo The number must be greater than 'null'.
      goto:eof
    )
    ::variables
    set "a=0"
    set "b=1"
    set "c="
    set "i=0"
    ::cycle to retrieve Fibonacci number
    :loop
      if "%i%" equ "%1" goto:result
      set /a "c=%a% + %b%"
      set /a "a=%b%"
      set /a "b=%c%"
      set /a "i+=1"
      goto:loop
    ::print result
    :result
    echo %b%
  endlocal
exit /b
