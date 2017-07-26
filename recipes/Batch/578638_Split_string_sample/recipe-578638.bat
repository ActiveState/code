@echo off
  setlocal enabledelayedexpansion
    set "str=this is a string"
    ::at firstly we need to know a length of string
    set "len=0"
    for /l %%i in (0, 1, 255) do (
      set "c=!str:~%%i!"
      if defined c set /a "len+=1"
    )
    ::now we are ready to split string on characters
    set /a "len-=1"
    for /l %%i in (0, 1, !len!) do (
      for /l %%j in (1, 1, 1) do echo."!str:~%%i,%%j!"
    )
  endlocal
exit /b
