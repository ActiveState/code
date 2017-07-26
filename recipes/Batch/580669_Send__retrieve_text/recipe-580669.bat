@echo off
setlocal enabledelayedexpansion

::type the script listing to the clipboard
type "%~dpnx0" |clip  
echo.
echo listing of this script saved to clipboard, now you can paste it to notepad
echo.
echo.
echo.
echo retrieving the listing from notepad. FOR /F skips the empty lines...
echo.
echo.
set jsfunc=new ActiveXObject('htmlfile').parentWindow.clipboardData.getData('text')
set dialog="javascript:close(new ActiveXObject('Scripting.FileSystemObject').
set dialog=%dialog%GetStandardStream(1).Writeline(%jsfunc%))"

for /f "TOKENS=*" %%p in ('mshta.exe %dialog%') do echo %%p
echo Done!
