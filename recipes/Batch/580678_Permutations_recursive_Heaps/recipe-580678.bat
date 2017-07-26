@echo off
setlocal enabledelayedexpansion  
set arr=ABCD
call :permu  4 arr
goto:eof

:permu num  &arr
if %1 equ 1 call echo(!%2! & exit /b
setlocal
set /a "num=%1-1,n2=num-1"
set arr=!%2!
for /L %%c in (0,1,!n2!) do (
   call:permu !num! arr 
   set /a  n1="num&1"
   if !n1! equ 0 (call:swapit !num! 0 arr) else (call:swapit !num! %%c arr)
   )
   call:permu !num! arr
endlocal & set %2=%arr%
exit /b

:swapit  from  to  &arr
setlocal
set arr=!%3!
set temp1=!arr:~%~1,1!
set temp2=!arr:~%~2,1!
set arr=!arr:%temp1%=@!
set arr=!arr:%temp2%=%temp1%!
set arr=!arr:@=%temp2%!
:: echo %1 %2 !%~3! !arr!
endlocal & set %3=%arr%
exit /b
