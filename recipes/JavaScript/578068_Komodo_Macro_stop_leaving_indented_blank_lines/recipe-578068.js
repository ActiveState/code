/*

Blank Newlines Macro for Komodo

This macro automatically removes blank new lines when you press enter,
while keeping the indentation level the same.

Copied original structure from http://code.activestate.com/recipes/577790/

Installation:
    * Find the toolbox
    * Right-click and choose "Add" > "New Macro"
    * Give it a name, keep Javascript selected
    * Paste this entire file into the text box
    * Go to Triggers and set it to trigger on startup 
    * Execute the macro so you can use it without restarting Komodo

*/

if (typeof(window.extensions) == 'undefined') {
    window.extensions = {};
}

if (extensions.blanknewlines && extensions.blanknewlines.onkeypress_handler) {
    // Remove the existing trigger handler, we'll re-instate it.
    var editor_pane = ko.views.manager.topView;
    editor_pane.removeEventListener('keypress', extensions.blanknewlines.onkeypress_handler, true);
}
extensions.blanknewlines = {};


(function() {

    var log = ko.logging.getLogger("blanknewlines");
    log.setLevel(ko.logging.LOG_DEBUG);

    var charCodeEnter = 13;

    this.onkeypress_handler = function(e) {
        try {

            // Abort if it wasn't the Enter key.
            if (e.which != charCodeEnter && e.keyCode != charCodeEnter) {
                return;
            }

            // Only trap keypresses that originated in the editor.
            if (e.getPreventDefault()) {
                // Somebody else already tried to cancel this event.
                return;
            }

            // Create shorthands for 'currentView'
            var view = ko.views.manager.currentView;
            if (e.originalTarget.localName != "scintilla" &&
                e.originalTarget != view.scintilla._embed) {
                // The event belongs to something else.
                return;
            }
            if (view.scintilla.key_handler) {
                // There is a specialized key handler registered, don't do
                // anything, as Komodo's likely in interactive search mode.
                return;
            }

            /**
             * @type {Components.interfaces.ISciMoz}
             */
            var editor = view.scimoz;

            // Abort if there is a selection.
            if (editor.selText.length) {
                return;
            }

            // Get the current line number.
            var lineNumber = editor.lineFromPosition(editor.currentPos);

            // Abort if cursor is not at the end of the line.
            if (editor.currentPos != editor.getLineEndPosition(lineNumber)) {
                return;
            }

            // Get the current line's text.
            var lineBuffer = new Object();
            editor.getLine(lineNumber, lineBuffer);
            var lineText = String(lineBuffer.value);

            // Abort if the line is not just whitespace.
            if (!lineText.match(/^\s+\r?\n?$/)) {
                return;
            }

            if (lineText.length <= 1) {

                // The user has pressed the enter key on a blank line with
                // no whitespace at all.

                // I don't like how Komodo will auto-indent in this case.
                // If you do like it, then uncomment the next line.
                // return;

                // Insert a simple new line, avoiding the auto-indent.

                editor.newLine();

            } else {

                // The user has pressed the enter key on a line that
                // contains only whitespace.

                // Insert an empty new line before the current line. This will
                // make a new blank line appear, and push the the existing
                // indented line downwards.

                editor.home();
                editor.newLine();
                editor.lineEnd();

            }

            e.preventDefault();
            e.stopPropagation();

        } catch(ex) {
            log.exception(ex);
        }

    }

    // Hook up the keypress event listener.
    var editor_pane = ko.views.manager.topView;
    editor_pane.addEventListener('keypress', this.onkeypress_handler, true);

}).apply(extensions.blanknewlines);
