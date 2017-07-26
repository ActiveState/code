komodo.assertMacroVersion(2);
if (komodo.view && komodo.view.scintilla) { komodo.view.scintilla.focus(); }

// Get the editor object into a variable. It's used in the validator function.
var editor = ko.views.manager.currentView.scimoz;
var buffer_length = editor.length;

// Ask the user for the character position.
var response = ko.dialogs.prompt( 'Go to character', 'Enter character number', buffer_length, 'Go to character',
                                  'mruName1', validate_new_pos, false );
// If they entered one, go to that position. We know it'll be valid because of the validator.
if ( response != null ) {
    response = response.toString();
    response = parseInt( response, 10 );
    editor.gotoPos( response );
}

// Function to validate the entry. First, it must be an integer; then it must be between 0 and
// <length of buffer>. If it's invalid, tell the user why.
function validate_new_pos( p_unknown, p_value ) {
    var ret_val = true;
    if ( p_value != parseInt(p_value, 10 ).toString() ) {
        ret_val = false;
    } else {
        l_value = parseInt(p_value, 10 );
        if ( l_value < 0 || l_value > buffer_length ) {
            ret_val = false;
        }
    }
    if ( ! ret_val ) {
        alert( 'You must enter an integer between 0 and ' + buffer_length );
    }
    return ret_val;
}
