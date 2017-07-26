@ECHO off
REM MessengerMain.bat
TITLE Messanger Setup
SET /p name= Name: 

:addressChoice
ECHO.
ECHO  Enter one of the numbers below
ECHO.
ECHO  1. Use current address
ECHO  2. Enter a new address
ECHO.
SET /p newAddress= Choice? 
IF %newAddress%==1 (
SET address=C:\Users\Dad\Documents\School\BatchMSG\MSGFolder
GOTO mainPart
)
IF %newAddress%==2 GOTO addressLoop
IF %newAddress% GTR 2 (
CLS
ECHO ERROR: Enter either 1 or 2
GOTO addressChoice
)
IF %newAddress% LSS 1 (
CLS
ECHO Enter either 1 or 2
GOTO addressChoice
)

:addressLoop
SET /p address= Address: 
IF NOT EXIST %address% (
ECHO  Please enter a valid address
GOTO addressLoop
)

:mainPart
CLS
ECHO  This is a list of all current conversations in %address%:
ECHO.
DIR %address% /B | FIND ".txt"
ECHO.
ECHO  You may choose an existing filename from the list above
ECHO  or enter a new filename
ECHO.
SET /p convoDest= Enter Filename: 

ECHO %address%\%convoDest% > Address.txt
ECHO %name% > Name.txt
IF NOT EXIST %address%\%convoDest% (
ECHO. 2>%address%\%convoDest%
)

START Receiver.bat
START Sender.bat
------------------------------
@ECHO off
REM Receiver.bat
FOR /f %%a IN (Address.txt) DO (
SET address=%%a
)
FOR /f "usebackq delims=" %%a IN (Name.txt) DO (
SET name=%%a
)
TITLE Receiver: %name% - %address%
SET /a counterOld=0

:mainReader
SET /a counter=0
IF NOT EXIST %address% (
ECHO Somebody has deleted the conversation
PAUSE
EXIT
)
FOR /f %%a IN (%address%) DO (
SET /a counter+=1
)
IF NOT %counter%==%counterOld% ( 
CLS
TYPE %address%
COLOR FC
PING 1.1.1.1 -n 1 -w 800 >NUL
COLOR 07
SET /a counterOld=%counter%
)
GOTO mainReader
------------------------------
@ECHO off
REM Sender.bat
FOR /f %%a IN (Address.txt) DO (
SET address=%%a
)
FOR /f "usebackq delims=" %%a IN (Name.txt) DO (
SET name=%%a
)
DEL Address.txt
DEL Name.txt
TITlE Sender: %name% - %address%
ECHO  Enter /cls to clear the conversation
ECHO  Enter /del to delete the conversation
ECHO.

:mainPart
SET /p msg= Message: 
@ECHO %name%: %msg%>>%address%
IF "%msg%"=="/cls" (
ECHO. 2>%address%
)
IF "%msg%"=="/del" (
DEL %address%
CLS
ECHO You have ended the conversation
PAUSE
EXIT
)
CLS
GOTO mainPart
