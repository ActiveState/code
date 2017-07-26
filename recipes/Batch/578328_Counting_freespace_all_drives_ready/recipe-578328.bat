@echo off
  setlocal
    ::possible drive letters list
    set "map=A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    ::looking for drives with ready status
    for %%i in (%map%) do (
      dir %%i:\ 2>nul 1>nul && call:freespace %%i
    )
  endlocal
exit /b

::this function provides free space checking
:freespace
  for /f "tokens=3" %%i in ('dir /-c %1:\') do set "len=%%i"
  echo Drive   Freespace
  echo -----   ---------------------
  echo  %1:\     %len% (bytes)
  echo.
exit /b 0
