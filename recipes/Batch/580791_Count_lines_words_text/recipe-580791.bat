::counts lines and words in a text file
@echo off

set /a cnt=0,lin=0
for /f "usebackq tokens=*" %%a in (%1) do ( set /a lin+=1
  for  %%b in (%%a) do  set /a cnt+=1 
)  
echo  File: %~nx1  words: %cnt%  lines: %lin%

pause
