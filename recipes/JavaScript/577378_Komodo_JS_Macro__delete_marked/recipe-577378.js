var view = ko.views.manager.currentView;
var scimoz = view.scimoz;
view.scintilla.focus();
view.setFocus();
var currentPos = scimoz.currentPos;
var bmNum = ko.markers.MARKNUM_BOOKMARK;
var bmmask = 1 << bmNum;
var linesToDelete = [];
var nextLine = -1;
while (true) {
    nextLine = scimoz.markerNext(nextLine + 1, bmmask);
    if (nextLine == -1) {
        break;
    }
    linesToDelete.push(nextLine);
}
scimoz.beginUndoAction();
try {
    while (linesToDelete.length) {
        var lineToDelete = linesToDelete.pop();
        scimoz.markerDelete(lineToDelete, bmNum);
        var startPos = scimoz.positionFromLine(lineToDelete);
        var endPos = scimoz.positionFromLine(lineToDelete + 1);
        var docLen = scimoz.length;
        if (endPos > docLen) endPos = docLen;
        scimoz.targetStart = startPos;
        scimoz.targetEnd = endPos;
        scimoz.replaceTarget(0, "");
    }
} catch(ex) {
    alert("Error removing lines: " + ex);
} finally {
    scimoz.endUndoAction();
}
scimoz.currentPos = scimoz.anchor = currentPos;
