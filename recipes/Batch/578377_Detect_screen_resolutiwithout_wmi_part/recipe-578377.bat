@set @script=0 /*
  @echo off
    set @script=
    cscript //nologo //e:jscript "%~dpnx0"
  exit /b
*/

var screen = {
  getResolution : function() {
    with (new ActiveXObject('htmlfile')) {
      var scr = parentWindow.screen;
      WScript.echo(scr.width + 'x' + scr.height);
    }
  }
};

screen.getResolution();
