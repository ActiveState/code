@echo off
  setlocal
    rem looking for PowerShell code
    for /f "tokens=* delims=:" %%i in ('findstr "^::" "%~dpnx0"') do (
      rem and  store it at *.ps1 file
      1>>script.ps1 (echo.%%i)
    )
    rem executing PowerShell script
    powershell /nologo /noprofile /noexit /file script.ps1
    rem remove *.ps1 file after closing host
    del /f /q "%~dp0script.ps1"
  endlocal
exit /b

:code
::$code = {
::  $regex = '\d{2}:\d{2}\d{2}'
::
::  do {
::    $clock = Get-Date -for 'HH:mm:ss'
::    $title = [Console]::Title
::
::    if ($title -match $regex) {
::      $fresh = $title -replace $regex
::    }
::    else {
::      $fresh = "$clock $title"
::    }
::
::    [Console]::Title = $fresh
::    sleep -sec 1
::  } while ($true)
::}
::
::$posh = [PowerShell]::Create()
::$null = $posh.AddScript($code)
::$posh.BeginInvoke() | out-null
