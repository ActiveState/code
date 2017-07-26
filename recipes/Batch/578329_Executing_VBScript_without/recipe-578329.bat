@set @env=0 /*
  @echo off
    set @env=
    cscript //nologo //e:jscript "%~dpnx0"
  exit /b
'intBig = 100
'intLow = 1
'
'For i = 1 To 5
'  Randomize
'  intRes = Int((intBig - intLow + 1) * Rnd + intLow)
'  WScript.Echo intRes
'Next
*/

with (new ActiveXObject('Scripting.FileSystemObject')) {
  with (new ActiveXObject('MSScriptControl.ScriptControl')) {
    var f, s, code = "";
    f = OpenTextFile(WScript.ScriptFullName, 1);
    while (!f.AtEndOfStream) {
      s = f.ReadLine();
      if (s.match(/^\'(\w+|\s+|\=*.)+$/g)) code += s;
    }
    f.Close();
    
    language = 'VBScript';
    addobject('WScript', WScript, true);
    addcode(code.split(/'/).join('\n'));
  }
}
