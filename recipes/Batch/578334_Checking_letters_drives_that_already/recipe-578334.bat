@echo off
  setlocal
    ::possible drive letters
    set "map=A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    ::checking!!!
    for %%i in (%map%) do @%%i: 2>nul && echo %%i:\
  endlocal
exit /b
