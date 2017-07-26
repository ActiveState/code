@echo off
  call:endpoint tcp
  call:endpoint udp
exit /b

:endpoint
 <nul set /p res=%1: & (netstat -an | find /i /c "%1")
exit /b 0
