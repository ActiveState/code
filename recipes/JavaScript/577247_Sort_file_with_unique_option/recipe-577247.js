// Macro recorded on: Wed May 26 2010 15:54:13 GMT+0100 (GMT)
komodo.assertMacroVersion(2);
if (komodo.view && komodo.view.scintilla) { komodo.view.scintilla.focus(); }

var scimoz = ko.views.manager.currentView.scimoz;
var whole_buffer = scimoz.text;
var buffer_lines = whole_buffer.split( '\n' );
buffer_lines.sort();
if ( confirm( 'Unique?' ) ) {
    // Go through the array in reverse order from last to 2nd, and if the nth line is the same
    // as the (n-1)th line, then remove the nth line.
    for( bidx = buffer_lines.length - 1 ; bidx > 0 ; bidx-- ) {
        if ( buffer_lines[ bidx ] == buffer_lines[ bidx - 1 ] ) {
            buffer_lines.splice( bidx, 1 );
        }
    }
}
var new_buffer = buffer_lines.join( '\n' );
scimoz.selectAll();
scimoz.replaceSel( new_buffer );
