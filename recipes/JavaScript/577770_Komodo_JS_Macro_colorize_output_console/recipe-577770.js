var Cc = Components.classes, Ci = Components.interfaces;
var schemeSvc = Cc["@activestate.com/koScintillaSchemeService;1"].getService(Ci.koIScintillaSchemeService);
var darkScheme = schemeSvc.getScheme("Dark");

var command_output = document.getElementById('runoutput-scintilla');
if (!command_output) {
    // Might be Komodo 7 - as a sub-pane.
    command_output = document.getElementById('runoutput-desc-tabpanel').contentDocument.getElementById('runoutput-scintilla');
}
var scimoz = command_output.scimoz;
var language = "Text";
var encoding = "utf-8";
var alternateType = false;
darkScheme.applyScheme(scimoz, language, encoding, alternateType);
