try {
    var pv = document.getElementById('projectview');
    var part = pv.getSelectedItem();
    if (!part) {
        ko.dialogs.alert("No file selected");
        return;
    } else if (part.type != 'file') {
        ko.dialogs.alert("Only files can be copied.  Current item is: " +
                         part.type);
        return;
    }
    var osPathSvc = Components.classes["@activestate.com/koOsPath;1"].getService(Components.interfaces.koIOsPath);
    var fileObj = part.getFile();
    var dirName = fileObj.dirName;
    var baseName = fileObj.baseName;
    var copyPath = osPathSvc.join(dirName, "Copy of " + baseName);
    if (osPathSvc.exists(copyPath)) {
        ko.dialogs.alert("File '" + copyPath + "' already exists, not copying");
        return;
    }
    var shUtilSvc = Components.classes["@activestate.com/koShUtil;1"].getService(Components.interfaces.koIShUtil);
    shUtilSvc.copyfile(fileObj.path, copyPath);
    var p = ko.projects.manager.getSelectedProject();
    if (!p.live) {
        ko.dialogs.alert("Project "
                         + p.name
                         + " isn't live, so you'll have to manually add the copied file");
    } else {
        ko.projects.manager.refreshView();
    }
} catch(ex) {
    ko.dialogs.alert("Error: " + ex);
}
