function getCurrentMethodName() {
    var view = ko.views.manager.currentView;
    var scimoz = view.scimoz;
    var ciBuf = view.koDoc.ciBuf;
    var x = ciBuf.curr_section_from_line(view.currentLine);
    return x.title;
}

var s;
try {
    s = getCurrentMethodName();
} catch(ex) {
    s = "Failed getCurrentMethodName: " + ex;
}
alert(s);
