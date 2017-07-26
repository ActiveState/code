function relativePath(fromPath, toPath)
{
    var nsFileFrom = Components.classes["@mozilla.org/file/local;1"]
                          .createInstance(Components.interfaces.nsILocalFile);
    nsFileFrom.initWithPath(fromPath);
    var nsFileTo = Components.classes["@mozilla.org/file/local;1"]
                          .createInstance(Components.interfaces.nsILocalFile);
    nsFileTo.initWithPath(toPath);
    return nsFileTo.getRelativeDescriptor(nsFileFrom);
}

var currentView = ko.views.manager.currentView;
var doc = currentView.koDoc || currentView.document;  // Support both K6- and K7+
var cwd = doc.file.dirName;
var path = ko.filepicker.openFile(cwd);
if (path) {
    var relpath = relativePath(cwd, path);
    var editor = currentView.scimoz;
    editor.insertText(editor.currentPos, relpath);
}
