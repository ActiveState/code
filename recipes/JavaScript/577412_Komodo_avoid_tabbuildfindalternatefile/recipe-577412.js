var view = ko.views.manager.currentView;
var file = view.document.file;
var path = ko.filepicker.browseForFile(file.dirName,
                                        file.baseName,
                                        "file to replace");
if (!path) return;
ko.views.manager.doFileOpenAsync(path, 'editor', null, -1,
    function(newView) {
        if (newView) {
            view.close();
            newView.makeCurrent();
        }
    });
