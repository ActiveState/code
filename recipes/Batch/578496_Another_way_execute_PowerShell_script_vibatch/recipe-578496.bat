@echo off
  setlocal
    for /f "tokens=1 delims=:" %%i in ('^
      findstr /l /b /n /c:"exit /b" "%~dpnx0"') do set "n=%%i"
    more +%n% "%~dpnx0">>foo.ps1
    powershell /nologo /noprofile /noexit .\foo.ps1
  endlocal
exit /b
#PowerShell script begin
function Add-Clock {
  $code = {
    $reg = '\d{2}:\d{2}:\d{2}'
    do {
      $now = Get-Date -format 'HH:mm:ss'
      $old = [Console]::Title

      if ($old -match $pattern) {
        $new = $old -replace $pattern, $now
      }
      else {
        $new = "$now $old"
      }

      [Console]::Title = $new
      Start-Sleep -seconds 1
    } while ($true)
  }

  $ps = [PowerShell]::Create()
  [void]$ps.AddScript($code)
  $ps.BeginInvoke()
}

Add-Clock | Out-Null
Remove-Item .\foo.ps1
