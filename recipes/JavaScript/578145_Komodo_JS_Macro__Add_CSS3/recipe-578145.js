(function () {

var koView = ko.views.manager.currentView.scimoz;
var currentPos = koView.currentPos;

try {
    // Group operations into a single undo
    koView.beginUndoAction();

	var prefixes = [ '', '-o-', '-ms-', '-moz-', '-webkit-' ];

    var addPrefixes = function (line) {
		var build = '';
		for ( var i = 0, len = prefixes.length; i < len; i++ ) {
			ko.commands.doCommand('cmd_lineOrSelectionDuplicate');
			ko.commands.doCommand('cmd_home');
			ko.commands.doCommand('cmd_selectEnd');
			build = prefixes[i] + line;
			koView.replaceSel( build );
		}
    };

	ko.commands.doCommand('cmd_home');
	ko.commands.doCommand('cmd_selectEnd');

    if ( !!koView.selText ) {
       addPrefixes( koView.selText );
    }

}
catch (e) {
    alert(e);
}
finally {
    // Must end undo action or may corrupt edit buffer
    koView.endUndoAction();
}
})();
