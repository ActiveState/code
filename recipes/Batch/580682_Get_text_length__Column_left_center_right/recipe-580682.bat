@echo off
setlocal enabledelayedexpansion
mode con cols=103

echo Given$a$text$file$of$many$lines,$where$fields$within$a$line$ >file.txt
echo are$delineated$by$a$single$'dollar'$character,$write$a$program! >>file.txt
echo that$aligns$each$column$of$fields$by$ensuring$that$words$in$each$>>file.txt
echo column$are$separated$by$at$least$one$space.>>file.txt
echo Further,$allow$for$each$word$in$a$column$to$be$either$left$>>file.txt
echo justified,$right$justified,$or$center$justified$within$its$column.>>file.txt

for /f "tokens=1-13 delims=$" %%a in ('type file.txt') do (
 call:maxlen %%a %%b %%c %%d %%e %%f %%g %%h %%i %%j %%k %%l %%m  )
echo. 
for /f "tokens=1-13 delims=$" %%a in ('type file.txt') do (
 call:align 1 %%a %%b %%c %%d %%e %%f %%g %%h %%i %%j %%k %%l %%m  ) 
echo.
for /f "tokens=1-13 delims=$" %%a in ('type file.txt') do (
 call:align 2 %%a %%b %%c %%d %%e %%f %%g %%h %%i %%j %%k %%l %%m  )  
echo.
for /f "tokens=1-13 delims=$" %%a in ('type file.txt') do (
 call:align 3 %%a %%b %%c %%d %%e %%f %%g %%h %%i %%j %%k %%l %%m  )   
del file.txt   
exit /B

:maxlen     
  set "cnt=1"
:loop1
  if "%1"=="" exit /b
  call:strlen %1 length
  if !len%cnt%! lss !length! set len%cnt%=!length!
  set /a cnt+=1  
  shift
  goto loop1  
  
:align 
  setlocal   
  set cnt=1
  set print=
:loop2
  if "%2"=="" echo(%print%&endlocal & exit /b
  set /a width=len%cnt%,cnt+=1  
  set arr=%2
  if %1 equ 1 call:left   %width% arr
  if %1 equ 2 call:right  %width% arr
  if %1 equ 3 call:center %width% arr
  set "print=%print%%arr% "
  shift /2
  goto loop2  
 
:left %num% &string  
  setlocal
   set "arr=!%2!                     "
   set arr=!arr:~0,%1!
  endlocal & set %2=%arr%
exit /b
  
:right %num% &string  
  setlocal
   set "arr=                    !%2!"
   set arr=!arr:~-%1!
   endlocal & set %2=%arr%
exit /b
  
:center %num% &string  
setlocal
  set /a width=%1-1
  set arr=!%2!
  :loop3
  if "!arr:~%width%,1!"=="" set "arr=%arr% "
  if "!arr:~%width%,1!"=="" set "arr= %arr%"
  if "!arr:~%width%,1!"=="" goto loop3
endlocal & set %2=%arr%
exit /b  
   
:strlen  StrVar  &RtnVar
  setlocal EnableDelayedExpansion
  set "s=#%~1"
  set "len=0"
  for %%N in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
    if "!s:~%%N,1!" neq "" set /a "len+=%%N" & set "s=!s:~%%N!"
  )
  endlocal & set %~2=%len%
exit /b
