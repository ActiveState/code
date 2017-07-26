var pastebin = {
  post : function() {
    var selection = ko.views.manager.currentView.selection,
        lang = this.ko2pastebinLanguage(), properties, m,
        hop = Object.hasOwnProperty, url = [], xhr, response;

    if (selection == "") {
      return;
    }

    properties = {
      'format'      : lang,
      'code'        : selection,
      'name'        : ko.interpolate.interpolateString('%f', false, 'Filename'),
      'expire_date' : "1D", // {N: never, 10M: 10 minutes, 1H: 1 hour, 1D: 1 day, 1M: 1 month}
      'subdomain'   : "subdomain",
      'private'     : 1, // 0: public, 1: private,
      ''            : 'Send'
    };

    for (m in properties) {
      if (hop.call(properties, m)) {
        url.push([
          'paste',
          m ? '_' + m : '',
          '=',
          encodeURIComponent(properties[m])
        ].join(''));
      }
    }

    xhr = new XMLHttpRequest();
    xhr.open("post", "http://pastebin.com/api_public.php", false);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(url.join('&'));

    response = this.getReturnURL(xhr);
    this.copyText(response);
    ko.statusBar.AddMessage("Url " + response
                + " copied on clipboard using lang " + lang,
                "pastebin_macro", 10000, true)
  },

  getReturnURL : function(xhr) {
    return xhr.responseText;
  },

  copyText : function(str) {
    Components.classes["@mozilla.org/widget/clipboardhelper;1"]
      .getService(Components.interfaces.nsIClipboardHelper)
      .copyString(str);
  },

  ko2pastebinLanguage : function() {
    var language, langMap = {
      'ABAP' : 'abap',
      'ASM (NASM based)' : 'asm',
      'ASP' : 'asp',
      'ActionScript' : 'actionscript',
      'Ada' : 'ada',
      'Apache Log File' : 'apache',
      'AppleScript' : 'applescript',
      'AutoIt' : 'autoit',
      'BNF' : 'bnf',
      'Bash' : 'bash',
      'Blitz Basic' : 'blitzbasic',
      'C for Macs' : 'c_mac',
      'C#' : 'csharp',
      'C' : 'c',
      'C++' : 'cpp',
      'CAD DCL' : 'caddcl',
      'CAD Lisp' : 'cadlisp',
      'CSS' : 'css',
      'ColdFusion' : 'cfm',
      'D' : 'd',
      'DOS' : 'dos',
      'Delphi' : 'delphi',
      'Diff' : 'diff',
      'Eiffel' : 'eiffel',
      'Erlang' : 'erlang',
      'Fortran' : 'fortran',
      'FreeBasic' : 'freebasic',
      'Game Maker' : 'gml',
      'Genero' : 'genero',
      'Groovy' : 'groovy',
      'HTML' : 'html4strict',
      'Haskell' : 'haskell',
      'INI file' : 'ini',
      'Inno Script' : 'inno',
      'Java' : 'java',
      'JavaScript' : 'javascript',
      'Latex' : 'latex',
      'Linden Scripting Language' : 'lsl2',
      'Lisp' : 'lisp',
      'Lua' : 'lua',
      'M68000 Assembler' : 'm68k',
      'MPASM' : 'mpasm',
      'MatLab' : 'matlab',
      'MySQL' : 'mysql',
      'NullSoft Installer' : 'nsis',
      'OCaml' : 'ocaml',
      'Objective C' : 'objc',
      'Openoffice.org BASIC' : 'oobas',
      'Oracle 8' : 'oracle8',
      'PHP' : 'php',
      'PL/SQL' : 'plsql',
      'Pascal' : 'pascal',
      'Perl' : 'perl',
      'Python' : 'python',
      'QBasic/QuickBASIC' : 'qbasic',
      'Rails' : 'rails',
      'Robots' : 'robots',
      'Ruby' : 'ruby',
      'SQL' : 'sql',
      'Scheme' : 'scheme',
      'Smalltalk' : 'smalltalk',
      'Smarty' : 'smarty',
      'TCL' : 'tcl',
      'Text' : 'text',
      'VB.NET' : 'vbnet',
      'VisualBasic' : 'vb',
      'VisualFoxPro' : 'visualfoxpro',
      'XML' : 'xml',
      'XUL' : 'xml',
      'Z80 Assembler' : 'z80',
      'mIRC' : 'mirc',
      'unrealScript' : 'unreal'
    };

    language = langMap[ko.views.manager.currentView.document.language];
    if (!language) {
      return "text";
    }
    return language;
  }

};
pastebin.post();
