if (komodo.view && komodo.view.scintilla) { komodo.view.scintilla.focus(); }
var scimoz = ko.views.manager.currentView.scimoz;
var curr_line = scimoz.lineFromPosition(scimoz.currentPos);
var line_count = scimoz.lineCount;
if (curr_line == line_count - 1) {
    // At end of buffer
    return;
} else if (curr_line == line_count - 2) {
    var lastLinePos = scimoz.getLineEndPosition(line_count - 1);
    if (lastLinePos == scimoz.length) {
        alert("Last line in the buffer needs to end with a newline");
        return;
    }
}
scimoz.beginUndoAction();
try {
    scimoz.lineCut();
    scimoz.lineDown();
    scimoz.paste();
    scimoz.lineUp();
} finally {
    scimoz.endUndoAction();
}
