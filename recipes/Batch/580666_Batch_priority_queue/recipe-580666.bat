@echo off
setlocal enabledelayedexpansion

call :push 10  "item ten"
call :push 2   "item two"
call :push 100 "item one hundred"
call :push 5   "item five"

call :pop & echo !order! !item!
call :pop & echo !order! !item!
call :pop & echo !order! !item!
call :pop & echo !order! !item!
call :pop & echo !order! !item!

goto:eof


:push
set temp=000%1
set queu%temp:~-3%=%2
goto:eof

:pop
set queu >nul 2>nul
if %errorlevel% equ 1 (set order=-1&set item=no more items & goto:eof)  
for /f "tokens=1,2 delims==" %%a in ('set queu') do set %%a=& set order=%%a& set item=%%~b& goto:next
:next
set order= %order:~-3%
goto:eof
    
