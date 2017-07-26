var view = ko.views.manager.currentView;
var scimoz = view.scimoz;
var methodName = "*ext*verticalEditing";
if (!(methodName in view)) {
    view[methodName] = function(event) {
        if (event.keyCode == event.DOM_VK_DOWN) {
            var currentLine = scimoz.lineFromPosition(scimoz.currentPos);
            if (currentLine >= scimoz.lineCount - 1) {
                toggleOff();
                return;
            }
            var targetPos = scimoz.positionFromLine(currentLine + 1) + methodObject.columnPos;
            scimoz.gotoPos(targetPos);
            event.preventDefault();
            event.stopPropagation();   
        } else if (event.keyCode == event.DOM_VK_ESCAPE) {
            toggleOff();
        }
    };
    view[methodName].active = false;
    var macro = ko.macros.current;
    view[methodName].macro = macro;
    view[methodName].orig_iconurl = macro.iconurl;
}
var methodObject = view[methodName];

function toggleOn() {
    view.addEventListener('keypress', methodObject, true);
    methodObject.active = true;
    if (komodo.view) {
        komodo.view.setFocus();
        if (komodo.view.scintilla) { komodo.view.scintilla.focus(); }
    }
    methodObject.columnPos = scimoz.getColumn(scimoz.currentPos);
    methodObject.macro.iconurl = 'chrome://komodo/skin/images/leftarrow.png';
    methodObject.macro.save();
    window.addEventListener('current_view_changed', toggleOff, false);
    window.addEventListener('view_closed', toggleOff, false);
    //dump("listen for a keypress event for column: " + methodObject.columnPos + "\n");
}

function toggleOff() {
    //dump("stop listen for a keypress event\n");
    view.removeEventListener('keypress', methodObject, true);
    window.removeEventListener('current_view_changed', toggleOff, false);
    window.removeEventListener('view_closed', toggleOff, false);
    methodObject.active = false;
    methodObject.macro.iconurl = methodObject.orig_iconurl;
    methodObject.macro.save();
}

if (!methodObject.active) {
    toggleOn();
} else {
    toggleOff();
}
