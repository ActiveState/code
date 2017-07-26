var view = ko.views.manager.currentView;
if (!('extensions' in ko)) {
    ko.extensions = {};
}
if (!('togglers' in ko.extensions)) {
    ko.extensions.togglers = {};
}
var methodName = "*[[%tabstop1:togglerName]]*" + view.uid;
var methodObject;
if (!(methodName in ko.extensions.togglers)) {
    var scimoz = view.scimoz;
    methodObject = ko.extensions.togglers[methodName] = function(event) {
		[[%tabstop0:code]]
        else if (event.keyCode == event.DOM_VK_ESCAPE) {
            methodObject.toggleOff();
        }
    };
    methodObject.active = false;
    var macro = ko.macros.current;
    methodObject.macro = macro;
    methodObject.orig_iconurl = macro.iconurl;
    
    methodObject.toggleOn = function() {
        view.addEventListener('keypress', methodObject, true);
        dump("[[%tabstop1]] on!\n");
        methodObject.active = true;
        methodObject.columnPos = scimoz.getColumn(scimoz.currentPos);
        methodObject.macro.iconurl = 'chrome://famfamfamsilk/skin/icons/[[%tabstop3:iconName]].png';
        methodObject.macro.save();
        window.addEventListener('current_view_changed', methodObject.toggleOff, false);
    }
    
    methodObject.toggleOff = function() {
        dump("[[%tabstop1]] off!\n");
        view.removeEventListener('keypress', methodObject, true);
        window.removeEventListener('current_view_changed', methodObject.toggleOff, false);
        methodObject.active = false;
        methodObject.macro.iconurl = "";
        methodObject.macro.save();
    }
    view.scintilla.focus();
} else {
    methodObject = ko.extensions.togglers[methodName];
}

if (!methodObject.active) {
    methodObject.toggleOn();
} else {
    methodObject.toggleOff();
}
[[%tabstop4://]]dump("Running macro " + methodObject.macro.id + "\n");
