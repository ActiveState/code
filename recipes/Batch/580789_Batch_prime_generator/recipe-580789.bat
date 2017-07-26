:: prime table using rotating multiples stored in environment
@echo off
setlocal enabledelayedexpansion 
mode con cols=90
set @25=-10
set /a num=7,inc1=4,cnt=0,inc2=0,num1=0, maxprime=10000
set lin=    0:
call:line 2 & call:line 3 & call:line 5

:nextnum


if defined @%num% ( 
  for %%i in (!@%num%!) do (
    if %%i lss 0  (set /a num1=%num%-%%i,"inc2=-%%i<<1") else (set /a num1=%num%+%%i,"inc2=-(%%i>>1)")
    call :aux !num1! !inc2!
  )
  set @%num%=
) else (
  call :line %num%
  set /a num1= num * num 
  if %inc1% equ 4 (set/a "inc2=num<<2") else (set /a "inc2=-(num<<1)")
  if !num1! leq %maxprime%   set @!num1!=!inc2! 
)
set /a num+=inc1, inc1=6-inc1
if %num% lss %maxprime% goto nextnum

echo %lin%
pause  & goto:eof

:aux 
 if %1 leq %maxprime%  set @%1=%2 !@%1!
goto:eof   

:line        formats output in 10 right aligned columns
set num2=       %1
set lin=%lin%%num2:~-8%
set /a cnt+=1,res1=(cnt%%10)
if %res1% neq 0 goto:eof
echo %lin% 
set cnt1=    %cnt%
set lin=%cnt1:~-5%:
goto:eof 
