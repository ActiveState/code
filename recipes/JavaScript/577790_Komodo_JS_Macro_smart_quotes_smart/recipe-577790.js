/**
 * @fileoverview  With an editor selection, pressing any of [ { ( " ' keys will
 *                place matching braces or quotes around the selected text.
 * @author        Todd Whiteman (toddw@activestate.com)
 * @version       0.5
 */

if (typeof(window.extensions) == 'undefined') {
    window.extensions = {};
}

if (extensions.smartbraces && extensions.smartbraces.onkeypress_handler) {
    // Remove the existing trigger handler, we'll re-instate it.
    var editor_pane = ko.views.manager.topView;
    editor_pane.removeEventListener('keypress', extensions.smartbraces.onkeypress_handler, true);
}
extensions.smartbraces = {};

(function() {

    var log = ko.logging.getLogger("SmartBraces");
    //log.setLevel(ko.logging.LOG_DEBUG);

    // The accepted keypress characters.
    var brace_charcodes =          ["{", "(", "[", "\"", "'"];
    var matching_brace_charcodes = ["}", ")", "]", "\"", "'"];

    this.onkeypress_handler = function(e) {
        try {
            // Only trap the required brace keys.
            var key = String.fromCharCode(e.charCode);
            var idx = brace_charcodes.indexOf(key);
            if (idx < 0) {
                log.debug("onkeypress_handler:: not one of the handled keys: " + key);
                return; // These are not the keys you are looking for.
            }

            // Only trap keypresses that aren't used with a modifier and
            // originated in the editor.
            if (!e.charCode || e.ctrlKey || e.altKey) return;
            if (e.getPreventDefault()) {
                // Somebody else already tried to cancel this event.
                log.debug("onkeypress_handler:: key already handled: " + key);
                return;
            }
            // Create shorthands for 'currentView'
            var view = ko.views.manager.currentView;
            var wanted_event = e.originalTarget.localName == "scintilla" ||
                                  e.originalTarget == view.scintilla._embed ||
                                  // Allow the Scintilla IME input as well.
                                  (e.originalTarget.localName == "input" &&
                                   (e.originalTarget.parentNode.parentNode ==
                                    view.scintilla.inputField));
            if (!wanted_event) {
                // The event belongs to something else.
                log.debug("onkeypress_handler:: event originated elsewhere: " + e.originalTarget.localName);
                return;
            }
            if (view.scintilla.key_handler) {
                // There is a specialized key handler registered, don't do
                // anything, as Komodo's likely in interactive search mode.
                log.debug("onkeypress_handler:: special key handler already installed");
                return;
            }

            log.debug("onkeypress_handler:: key: " + key);

            /**
             * @type {Components.interfaces.ISciMoz}
             */
            var editor = view.scimoz;

            // Don't do anything if there isn't a selection within the document.
            var selection = editor.selText;
            if (!selection) {
                return;
            }

            var anchor = editor.anchor;
            var cursorPos = editor.currentPos;
            editor.replaceSel(key + selection + matching_brace_charcodes[idx]);

            // Restore the selection.
            if (anchor < cursorPos) {
                editor.anchor = anchor;
                editor.currentPos = cursorPos + 2;
            } else {
                editor.anchor = anchor + 2;
                editor.currentPos = cursorPos;
            }

            // Stop the event from going to the editor as a regular keypress.
            e.preventDefault();
            e.stopPropagation();
        } catch(ex) {
            log.exception(ex);
        }
    }

    // Hook up the keypress event listener.
    var editor_pane = ko.views.manager.topView;
    editor_pane.addEventListener('keypress', this.onkeypress_handler, true);

}).apply(extensions.smartbraces);
