if (!('extensions' in ko)) ko.extensions = {};
if (!('toggers' in ko.extensions)) ko.extensions.togglers = {};
var methodName = "*ext*autoWrap";
var methodObject;
if (!(methodName in view)) {
    var view = ko.views.manager.currentView;
    var scimoz = view.scimoz;
    methodObject = ko.extensions.togglers[methodName] = function(event) {
        if (event.keyCode === 0 && event.charCode == event.DOM_VK_SPACE) {
            if (scimoz.getColumn(scimoz.currentPos) > 72) {
                komodo.doCommand('cmd_newline');
                event.preventDefault();
                event.stopPropagation();   
            }
        } else if (event.keyCode == event.DOM_VK_ESCAPE) {
            methodObject.toggleOff();
        }
    };
    methodObject.active = false;
    var macro = ko.macros.current;
    methodObject.macro = macro;
    methodObject.orig_iconurl = macro.iconurl;

    methodObject.toggleOn = function() {
        view.addEventListener('keypress', methodObject, true);
        methodObject.active = true;
        if (komodo.view) {
            komodo.view.setFocus();
            if (komodo.view.scintilla) { komodo.view.scintilla.focus(); }
        }
        methodObject.columnPos = scimoz.getColumn(scimoz.currentPos);
        methodObject.macro.iconurl = 'chrome://famfamfamsilk/skin/icons/bell.png';
        methodObject.macro.save();
        // Watching view.blur won't fire when the view is closed.
        window.addEventListener('current_view_changed', methodObject.toggleOff, false);
    }
    
    methodObject.toggleOff = function() {
        view.removeEventListener('keypress', methodObject, true);
        window.removeEventListener('current_view_changed', methodObject.toggleOff, false);
        methodObject.active = false;
        methodObject.macro.iconurl = methodObject.orig_iconurl;
        methodObject.macro.save();
    }
} else {
    methodObject = ko.extensions.togglers[methodName];
}

if (!methodObject.active) {
    methodObject.toggleOn();
} else {
    methodObject.toggleOff();
}
