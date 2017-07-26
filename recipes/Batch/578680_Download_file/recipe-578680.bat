@set @env=0 /*
  @echo off
    set @env=
    setlocal
      set "i=0"
      for %%i in (%*) do set /a "i+=1"
      if "%i%" equ "2" (
        cscript //nologo //e:jscript "%~dpnx0" %1 %2
      ) else (
        echo %~n0 v1.01 - download files from internet
        echo.
        echo Usage: %~n0 ^<local_path^> ^<url^>
        echo Example:
        echo    %~n0 E:\arc http://download.sysinternals.com/files/Autoruns.zip
      )
    endlocal
  exit /b
*/

with (WScript.Arguments) {
  with (new ActiveXObject('Scripting.FileSystemObject')) {
    var file = Unnamed(1).substring(Unnamed(1).lastIndexOf('/') + 1, Unnamed(1).length);
    
    if (FolderExists(Unnamed(0))) {
      with (new ActiveXObject('MSXML2.XMLHTTP.3.0')) {
        try {
          open('GET', Unnamed(1), false);
          send();
        }
        catch (e) {}
        
        if (status == 200) {
          with (new ActiveXObject('ADODB.Stream')) {
            Open();
            Type = 1;
            Write(responseBody);
            SaveToFile(Unnamed(0) + '\\' + file, 2);
            Close();
          }
        }
        else WScript.echo('Error: bad request.');
      }
    }
    else WScript.echo('Error: folder should be exist.');
  }
}
