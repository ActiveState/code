// Get the editor, current line and path details.
var scimoz = ko.views.manager.currentView.scimoz;
var linenum = scimoz.lineFromPosition(scimoz.currentPos);
var basename = ko.views.manager.currentView.koDoc.file.baseName;
var dirname = ko.views.manager.currentView.koDoc.file.dirName;

// Run the git blame process.
var runSvc = Components.classes["@activestate.com/koRunService;1"].
                createInstance(Components.interfaces.koIRunService);
var cmd = 'git blame ' + basename;
var process = runSvc.RunAndNotify(cmd, dirname, '', '');

// Wait till the process is done (synchronously).
var retval = process.wait(-1);
if (retval == 0) {
    var stdout = process.getStdout();
    var lines = stdout.split("\n");
    var re = new RegExp("([0-9a-f]*) \\((.*? [12][09][0-9]{2}-[0-9]{2}-[0-9]{2}) ");
    var match = re.exec(lines[linenum]);
    if (match) {
        cmd = 'git log --format=%s -n 1 ' + match[1];
        process = runSvc.RunAndNotify(cmd, dirname, '', '');
        retval = process.wait(-1);
        ko.statusBar.AddMessage("BLAME: " + match[2], "editor", 10000, true);
        if (retval == 0) {
            ko.statusBar.AddMessage( process.getStdout(), "editor", 10000, true);
        }
    }
}
