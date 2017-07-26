@set @script=0 /*
  @echo off
    set @script=
    cscript //nologo //e:jscript "%~dpnx0"
  exit /b
*/

with (new ActiveXObject('Microsoft.XMLHTTP')) {
   open('GET', 'http://internet.yandex.ru/', false);
   send();
   
   WScript.echo(responseText.match(/IPv4:\s(\d+\.){3}\d+/g));
}
