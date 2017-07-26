@echo off
  set "prompt=$$$S"
  ::additional extensions for which command
  set pathext | findstr /e /l ".CPL;.MSC" > nul
  if "%errorlevel%" equ "1" set "pathext=%pathext%;.CPL;.MSC"
  ::restore pathext variable
  if "%1" equ "/fixext" set "pathext=%pathext:~0,54%"
  setlocal enabledelayedexpansion
    ::get the logical end of batch
    for /f "tokens=1 delims=:" %%i in ('findstr /n /l "exit /b" "%~dpnx0"') do set /a "i=%%i+1"
    ::add bash style commands into cmd
    if "%1" equ "/bash" for /f "tokens=*" %%i in ('more +!i! "%~dpnx0"') do doskey %%i
    ::print all imported aliases
    if "%1" equ "/map" for /f "tokens=1 delims== " %%i in ('doskey /macros:all^
      ^| findstr /v ]$ ^| sort') do <nul set /p "map=%%i   "
  endlocal
exit /b
::aliases
clear=cls
cp=copy /y $1 $2 > nul
ed=edit $1
history=doskey /history
ls=for /f "skip=3 tokens=*" %i in ('dir /d /o:g /o:n $* ^| findstr /i [a-z]') do @echo.%i
mv=move /y $1 $2
now=echo %date% %time:~0,8%
printenv=set
pwd=cd
which=for %i in (%pathext%) do @for %j in ($1%i) do @if not "%~$PATH:j" equ "" @echo %~$PATH:j
whoami=echo %userdomain%\%username%
