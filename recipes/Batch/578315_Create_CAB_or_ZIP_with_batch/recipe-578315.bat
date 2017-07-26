@set @script=0 /*
  @echo off
    set @script=
    cscript //nologo //e:jscript "%~dpnx0" %1 %2
  exit /b
*/

with (WScript.Arguments.Named) {
  if (length != 2) {
    WScript.echo(WScript.ScriptName + " </a:archive> </f:folder>");
    WScript.Quit(1);
  }

  //validator extension of future archive
  RegExp.prototype.Validate = function() {
    var raw = this.exec(Item('a')),
        res = RegExp.lastMatch;
    return res.toUpperCase();
  }

  var fso = new ActiveXObject('Scripting.FileSystemObject'),
      app = new ActiveXObject('Shell.Application');

  //store files into .CAB or .ZIP files
  if ((new RegExp('.cab', 'i').Validate()) == '.CAB') {
    try {
      with (new ActiveXObject('MakeCab.MakeCab')) {
        CreateCab(Item('a'), false, false, false);

        with (new Enumerator(fso.GetFolder(Item('f')).Files)) {
          for (; !atEnd(); moveNext()) {
            var itm = item();
            AddFile(itm.Path, itm.Name);
          }
        }

        CloseCab();
      }
    }
    catch (e) { WScript.echo(e.message + '.'); }
  }
  else if ((new RegExp('.zip', 'i').Validate()) == '.ZIP') {
    try {
      var zip = fso.CreateTextFile(Item('a'), true);
      zip.Write('PK\05\06' + new Array(19).join('\0'));
      zip.Close();

      with (new Enumerator(fso.GetFolder(Item('f')).Files)) {
        for (; !atEnd(); moveNext()) {
          var itm = item();
          if (itm != fso.GetFile(Item('a')).Path) {
            app.NameSpace(fso.GetFile(Item('a')).Path).CopyHere(itm.Path);
            WScript.Sleep(1000);
            WScript.echo("File added: " + itm.Path);
          }
        }
      }
    }
    catch (e) { WScript.echo(e.message + '.'); }
  }
  else {
    WScript.echo("Unsupported archive format.");
    WScript.Quit(1);
  }
}
