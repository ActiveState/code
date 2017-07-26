@set @script=0 /*
  @echo off
    set @script=
    setlocal
      set "a=0"
      for %%i in (%*) do set /a "a+=1"
      if "%a%" equ "0" goto:interactive
      if "%a%" neq "1" goto:error
      if "%1" equ "/b" goto:error
      if "%1" neq ""   cscript //nologo //e:jscript "%~dpnx0" %1 & goto:eof
      :interactive
      cscript //nologo //e:jscript "%~dpnx0" "/b"
      echo Type "clear" to erase history or "exit" to leave session
      echo.
      :begin
        set /p "scanf=>>> "
        for %%i in ("/b", "/h") do (
          if "%scanf%" equ %%i echo =^>err & echo. & goto:begin
        )
        if "%scanf%" equ "exit"  goto:eof
        cscript //nologo //e:jscript "%~dpnx0" "%scanf%"
        if "%scanf%" equ "clear" cls
        echo.
      goto:begin
      :error
        echo =^>err
    endlocal
  exit /b
*/

var js = {
  printf : function($) { WScript.echo($); },
  
  banner : (function() { return (WScript.ScriptName +
           " v3.31 - converts hex to decimal and vice versa\n" +
           "Copyright (C) 2012-2013 greg zakharov gregzakh@gmail.com\n"); }
           )(),
           
  syntax : (function() { return ("\nUsage: " + WScript.ScriptName +
           " [decimal | hexadecimal]"); }
           )(),
           
  hex2dec : function($) {
    return Number($) ? '0x' + $.slice(2, $.length).toUpperCase() + ' = ' + Number($) : '=>err';
  },
  
  dec2hex : function($) {
    return Number($) ? $ + ' = 0x' + Number($).toString(16).toUpperCase() : '=>err';
  },
  
  chkData : function($) {
    if (/^\d+$/g.test($)) return this.dec2hex($);
    else if (/^(0x|x)|^[a-f0-9]+$/ig.test($))
      return !/x/i.test($.slice(0, 1)) ? (/0x/i.test($.slice(0, 2)) ? this.hex2dec($) :
                                               this.hex2dec('0x' + $)) : this.hex2dec('0' + $);
    else return '=>err';
  }
};

try {
  with (WScript.Arguments) {
    if (length == 1) {
      if (Named.Exists("b")) js.printf(js.banner);
      else if (Named.Exists("h")) js.printf(js.banner + js.syntax);
      else js.printf(js.chkData(Unnamed(0)));
    }
  }
}
catch (e) { js.printf('=>err'); }
