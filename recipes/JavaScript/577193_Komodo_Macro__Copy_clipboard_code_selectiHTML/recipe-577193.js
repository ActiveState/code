var view = ko.views.manager.currentView;

var tmpFileSvc = Components.classes["@activestate.com/koFileService;1"]
                 .getService(Components.interfaces.koIFileService)
fname = tmpFileSvc.makeTempName(".html");

var lang = view.document.languageObj;
var forceColor = true;
var selectionOnly = view.selection != "";
var schemeService = Components.classes['@activestate.com/koScintillaSchemeService;1'].getService();
schemeService.convertToHTMLFile(view.scimoz,
                                view.document.displayPath,
                                view.document.language,
                                lang.styleBits,
                                view.document.encoding.python_encoding_name,
                                fname,
                                selectionOnly,
                                forceColor);


var file = Components.classes["@activestate.com/koFileEx;1"]
        .createInstance(Components.interfaces.koIFileEx)
file.URI = ko.uriparse.localPathToURI(fname);
file.open('rb');
var str = file.readfile();
file.close();

str = str.replace(/\n|\r/g, "");
var m = str.match(/\s*[a-zA-Z0-9._-]*\s*{.*?}/g);
var styles = {};
for (var i in m) {
    var selector = m[i].match(/\s*([a-zA-Z0-9._-]*)\s*{(.*?)}/);
    if (selector && /^span\./.test(selector)) {
        styles[selector[1].substring("span.".length)] = selector[2].replace(/(^\s*|\s*$)/g, "");
    }
}

m = str.match(/(<span.*?)<\/body>/);
var result = m[1]

for (i in styles) {
    var style = styles[i];
    result = result.replace(new RegExp('<span class="' + i + '">', "g"), '<span style="' + style + '">');
}
result = result.replace(/&nbsp;/g, ' ') // OpenOffice Writer ignores nbsp
        //.replace(/<br ?\/>/g, '');

result = '<pre><span style="font-size:12px">' + result + '</span></pre>';
xtk.include("clipboard");

transferable = xtk.clipboard.addTextDataFlavor("text/html", result);
xtk.clipboard.copyFromTransferable(transferable);
