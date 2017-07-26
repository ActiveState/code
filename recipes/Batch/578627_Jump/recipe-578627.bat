@set @script=0 /*
  @echo off
    set @script=
    cscript //nologo //e:jscript "%~dpnx0" %1
  exit /b
*/

with (WScript.Arguments) {
  if (length != 1) {
    var obj = WScript.ScriptName.split(".")[0];
    WScript.echo(obj + " v1.01 - File and registry key quick accessor");
    WScript.echo("Copyright (C) 2010-2013 greg zakharov gregzakh@gmail.com");
    WScript.echo("\nUsage: " + obj + " <path>");
    WScript.echo("e.g.: " + obj + " hklm\\software\\microsoft\\windows");
    WScript.echo("e.g.: " + obj + " e:\\src");
    WScript.Quit(1);
  }

  var jmp = Unnamed(0),
      key = "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Applets\\Regedit\\LastKey";
  
  try {
    with (new ActiveXObject('WScript.Shell')) {
      if (jmp.match(/^HK(CR|CU|LM)/i)) {
        jmp = jmp.replace(/^HKCR/i, 'HKEY_CLASSES_ROOT');
        jmp = jmp.replace(/^HKCU/i, 'HKEY_CURRENT_USER');
        jmp = jmp.replace(/^HKLM/i, 'HKEY_LOCAL_MACHINE');
        
        RegWrite(key, jmp, 'REG_SZ');
        Run("regedit -m", 1, false);
      }
      else if (jmp.match(/^([a-z]\:|\.|\\)/i)) {
        Run("explorer /n, " + jmp, 1, false);
      }
      else throw "Invalid data in current context.";
    }
  }
  catch (e) { WScript.echo(e); }
}
