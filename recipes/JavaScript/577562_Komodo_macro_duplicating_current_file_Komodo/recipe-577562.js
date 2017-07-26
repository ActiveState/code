try {
    var viewMgr = ko.places.viewMgr;
    var uris = viewMgr.getSelectedURIs();
    if (uris.length != 1) {
        throw new Error("Can only copy one file at a time\n");
    }
    var idx = viewMgr.view.getRowIndexForURI(uris[0]);
    var parentIdx = viewMgr.view.getParentIndex(idx);
    var target_uri = (parentIdx == -1
                      ? ko.places.manager.currentPlace
                      : ko.places.viewMgr.view.getURIForRow(parentIdx));
    viewMgr._finishFileCopyOperation(uris, target_uri, parentIdx, true);
} catch(ex) {
    ko.dialogs.alert("Error in copy-current-file macro", ex.message)
}
