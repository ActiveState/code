@echo off
setlocal enabledelayedexpansion
set /p yr= Enter year:
echo. 
call:monthdays %yr% list 
set mm=1
for %%i in (!list!) do (
  call:calcdow !yr! !mm! %%i dow
  set/a lsu=%%i-dow
  set mf=0!mm!
  echo !yr!-!mf:~-2!-!lsu! 
  set /a mm+=1
)
exit /b

:monthdays yr &list
setlocal
call:isleap %1 ly
for /L %%i in (1,1,12) do (
  set /a "nn = 30 + ^!(((%%i & 9) + 6) %% 7) + ^!(%%i ^^ 2) * (ly - 2)
  set list=!list! !nn!
)
endlocal & set %2=%list%
exit /b

:calcdow yr mt dy &dow  :: 0=sunday
setlocal
set/a a=(14-%2)/12,yr=%1-a,m=%2+12*a-2,"dow=(%3+yr+yr/4-yr/100+yr/400+31*m/12)%%7"
endlocal & set %~4=%dow%
exit /b

:isleap yr &leap  :: remove ^ if not delayed expansion
set /a "%2=^!(%1%%4)+(^!^!(%1%%100)-^!^!(%1%%400))"
exit /b
