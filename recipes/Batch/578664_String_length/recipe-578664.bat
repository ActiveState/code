@echo off
  setlocal
    set "str=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    set "len=0"
    
    :loop
    if defined str (set str=%str:~1%& set /a len+=1 & goto:loop)
    
    echo String length: %len%
  endlocal
exit /b
