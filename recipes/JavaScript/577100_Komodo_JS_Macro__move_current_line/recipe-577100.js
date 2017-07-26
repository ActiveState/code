if (komodo.view && komodo.view.scintilla) { komodo.view.scintilla.focus(); }
var scimoz = ko.views.manager.currentView.scimoz;
if (scimoz.lineFromPosition(scimoz.currentPos) == 0) {
    return;
}
scimoz.beginUndoAction();
try {
    scimoz.lineCut();
    scimoz.lineUp();
    scimoz.paste();
    scimoz.lineUp();
} finally {
    scimoz.endUndoAction();
}
