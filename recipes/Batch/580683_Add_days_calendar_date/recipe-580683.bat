@ECHO OFF
setlocal enabledelayedexpansion
set /a y=2016, m=6, d=16 
call:addays -100 y m d
echo %y% %m% %d%
pause
exit /b

:addays  %n% &Y &m &d
setlocal
set /a y=!%2!,m=!%3!,d=!%4!
call:date2jdn  %y% %m% %d% jdn
set /a  jdn+=%1
call:jdn2date %jdn% y m d
endlocal & set /a %2=%y%,%3=%m%,%4=%d%
exit /b

:date2jdn %YYYY% %MM% %DD% &JDN -- gregorian date to jyulian day number
setlocal
IF %2 LSS 3 (SET /A MM=%2+12, YY=%1-1) else (set /a MM=%2, YY=%1)
SET /A A=YY/100, B=A/4, C=2-A+B, E=36525*(YY+4716)/100, F=306*(MM+1)/10, JDN=C+%3+E+F-1524
endlocal & set %~4=%JDN%
exit /b

:jdn2date %JDN% &YYYY &MM &DD -- julian day number to gregorian date
SETLOCAL  
set /a L= %~1+68569,     N= 4*L/146097, L= L-(146097*N+3)/4, I= 4000*(L+1)/1461001
set /a L= L-1461*I/4+31, J= 80*L/2447,  K= L-2447*J/80,      L= J/11
set /a J= J+2-12*L,      I= 100*(N-49)+I+L
ENDLOCAL & SET /a %~2=%I%, %~3=%J%,%~4=%K%
EXIT /b
