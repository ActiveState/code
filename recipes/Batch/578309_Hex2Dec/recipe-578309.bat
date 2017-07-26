@echo off
  ::interactive mode
  if "%1" equ "" (
    if not defined run goto:interactive
    goto:error
  )
  ::null results
  for %%i in ("0" "x0" "0x0") do if "%1" equ "%%~i" goto:null
  ::parsing argument(s)
  setlocal enabledelayedexpansion
    ::checking number of arguments
    set "arg=0"
    for %%i in (%*) do set /a "arg+=1"
    if "%arg%" neq "1" if not defined run goto:help
    if "%arg%" neq "1" if defined run goto:error
    ::get length of argument
    set "i=0"
    set "str=%1"
    for /l %%i in (0, 1, 255) do (
      set "chr=!str:~%%i!"
      if defined chr set /a "i+=1"
    )
    ::is it prefix or hex number starts without him
    if !i! equ 2 (
      if "%str:~0,1%" equ "x" set "str=0%str%" & goto:check
    )
    if !i! gtr 2 (
      if "%str:~0,1%" equ "0" if "%str:~1,1%" neq "x" goto:error
      if "%str:~0,1%" equ "0" if "%str:~1,1%" equ "x" goto:hex2dec
      if "%str:~0,1%" equ "x" set "str=0%str%" && goto:check
    )
    for %%i in (a b c d e f) do if "%str:~0,1%" equ "%%i" set "str=0x%str%" & goto:hex2dec

    :check
    2>nul set /a "res=%str%"
    if "%errorlevel%" equ "0" (
      if "%str%" equ "%res%" goto:dec2hex
      goto:hex2dec
    )
    echo "%str%" | findstr /r [0-9a-f] > nul
    if "%errorlevel%" equ "0" set "str=0x%str%" && goto:hex2dec
    goto:error

    :dec2hex
    set "map=0123456789ABCDEF"
    for /l %%i in (1, 1, 8) do (
      set /a "res=str & 15, str >>=4"
      for %%j in (!res!) do set "hex=!map:~%%j,1!!hex!"
    )
    for /f "tokens=* delims=0" %%i in ("!hex!") do set "hex=0x%%i"
    echo %1 = !hex! & goto:eof

    :hex2dec
    2>nul set /a "res=%str%"
    if "%errorlevel%" gtr "0" goto:error
    for /f "tokens=2,3" %%i in ('findstr "# " "%~dpnx0"') do set "str=!str:%%i=%%j!"
    if "%res%" neq "" if "%res%" neq "0" (echo %str% = %res%) else goto:error
  endlocal
exit /b

:error
  echo =^>err
exit /b 1

:null
  echo =^>nil
exit /b 0

:help
::Hex2dec v2.03 - converts hex to decimal and vice versa
::Copyright (C) 2012-2013 greg zakharov
::
::Usage: hex2dec [decimal | hexademical]
::
::Example 1:
::  C:\>hex2dec 0x017a
::  0x017A = 378
::You'll got the same result with x17a or 17a numbers.
::
::Example 2:
::  C:\>hex2dec 13550
::  13550 = 0x34EE
::
::Example 3:
::  C:\>hex2dec 23f
::  0x23F = 575
::
::Note: hex2dec starts with interactive mode if there is
::no argument.
for /f "tokens=* delims=:" %%i in ('findstr "^::" "%~dpnx0"') do echo.%%i
exit /b 0

rem :: Upper case chart ::
# a A
# b B
# c C
# d D
# e E
# f F
rem ::   End of chart   ::

:interactive
  ::interactive mode on
  echo Hex2dec v2.03 - converts hex to decimal and vice versa
  echo.
  echo Enter decimal or hexademical number and press Enter to
  echo take result. Use "exit" or "clear" commands to quit or
  echo to make host clear.
  echo.
  setlocal
    ::already launched marker
    set "run=true"
    :begin
    set /p "ask=>>> "
    cmd /c "%~dpnx0" %ask%
    if "%ask%" equ "clear" cls
    if "%ask%" equ "exit"  cls & goto:eof
    echo.
    goto:begin
  endlocal
exit /b
