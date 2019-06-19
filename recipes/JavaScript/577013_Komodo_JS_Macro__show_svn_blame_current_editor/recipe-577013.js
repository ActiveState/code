// Get the editor, current line and path details.
var scimoz = ko.views.manager.currentView.scimoz;
var linenum = scimoz.lineFromPosition(scimoz.currentPos);
var path = ko.views.manager.currentView.koDoc.displayPath;

// Run the svn blame process.
var runSvc = Components.classes["@activestate.com/koRunService;1"].
                createInstance(Components.interfaces.koIRunService);
var cmd = 'svn blame ' + path;
var process = runSvc.RunAndNotify(cmd, '', '', '');

// Wait till the process is done (synchronously).
var retval = process.wait(-1);
if (retval == 0) {
    var stdout = process.getStdout();
    var lines = stdout.split("\n");
    ko.statusBar.AddMessage("BLAME: " + lines[linenum], "editor", 10000, true);
}
