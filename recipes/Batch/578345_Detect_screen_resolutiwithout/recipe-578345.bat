@echo off
  mshta "javascript:res=screen.width+'x'+screen.height;alert(res);close();" 1 | more
exit /b
