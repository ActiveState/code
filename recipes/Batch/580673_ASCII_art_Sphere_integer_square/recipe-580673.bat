@echo off 
setlocal enabledelayedexpansion
mode con cols=80
 
set /a r=220,cent=340,r2=r/2
set "spaces=                                   "
set "block1=MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
set "block2=#########"
set "block3=XXXXXXXXX"
set "block4=ooooooooo"
set "block5=?????????"
set "block6=*********"
set "block7=~~~~~~~~~"
set "block8=---------"
 
set wy=0
set linea=
echo                           Batch-File ASCII Ball
echo. 
for /L %%y in (-%r%,10,%r%) do (
   set /a "w1=r*r-%%y*%%y"
   call:sqrt2 w1 w1 
   set /a "w1=14*w1/10,wy=(cent-w1),cnt=0,sp=wy/10,centre=cent/10-sp"
   call set "linea=%%spaces:~0,!sp!%%%%block1:~0,!centre!%%
   set /a wy=0,sum=0
   for %%i in (30 80 120 150 170 185 195 200) do (
        set /a "cnt+=1,wy2=(%%i+r2)*w1/r,ww=(wy2+5)/10-sum,wy=wy2,sum+=ww" 
        call set miblock=%%block!cnt!%% 
        call set "Linea=%%linea%%%%miblock:~0,!ww!%%"   
   )  
   call echo(!linea!
)
echo.  
exit /b 
 
:sqrt2   [num] [sqrt] calculates integer square root . By AAcini
set "s=!%~1!"
set /A "x=s/(11*1024)+40,x=(s/x+x)>>1,x=(s/x+x)>>1,x=(s/x+x)>>1,x=(s/x+x)>>1,x=(s/x+x)>>1,x+=(s-x*x)>>31
set %~2=%x%
exit /b 
