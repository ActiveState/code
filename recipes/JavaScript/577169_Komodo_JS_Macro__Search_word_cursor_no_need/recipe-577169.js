// Macro recorded on Tue Oct 30 2007 17:51:45 GMT+0100 (CET)
komodo.assertMacroVersion(2);
if (komodo.view) { komodo.view.setFocus() };
var searchText = komodo.editor.selText;
if (!searchText.length) {
    // if we are under a word use it
    var scimoz = ko.views.manager.currentView.scimoz;
    searchText = ko.interpolate.getWordUnderCursor(scimoz);
    if (!searchText.length) {
        // use last pattern used
        searchText = ko.mru.get("find-patternMru");
    }
}

// Search with last user find preferences
var findSvc = Components.classes["@activestate.com/koFindService;1"]
            .getService(Components.interfaces.koIFindService);
var context = Components.classes["@activestate.com/koFindContext;1"]
            .createInstance(Components.interfaces.koIFindContext);
context.type = findSvc.options.preferredContextType;
Find_FindNext(window, context, searchText);
