@echo off
  setlocal enabledelayedexpansion
    ::incremental varibale
    set "i=0"
    ::store filenames into array
    for /f "tokens=*" %%f in ('dir /b') do (
      set arr[!i!]=%%f & set /a "i+=1"
    )
    ::display all array items
    set arr
    ::just line
    echo.===================================
    ::print array items (from 0 till n)
    set "len=!i!"
    set "i=0"
    :loop
    echo !arr[%i%]! & set /a "i+=1"
    if %i% neq %len% goto:loop
  endlocal
  ::another way to create array arr.!i!=%%f
exit /b
