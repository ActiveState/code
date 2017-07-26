:: timing a function to the hundredth of second
@echo off
Setlocal EnableDelayedExpansion

call :clock

::function timed: fibonacci series.....................
set /a a=0 ,b=1,c=1
:loop
if %c% lss 2000000000 echo %c% & set /a c=a+b,a=b, b=c & goto loop
::.....................................................

call :clock

echo  Function executed in %timed% hundredths of second
goto:eof

:clock
if not defined timed set timed=0
for /F "tokens=1-4 delims=:.," %%a in ("%time%") do ( 
set /A timed = "(((1%%a - 100) * 60 + (1%%b - 100)) * 60 + (1%%c - 100))  * 100 + (1%%d - 100)- %timed%"
)
goto:eof
