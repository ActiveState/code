/*
 * This Source Code is subject to the terms of the Mozilla Public License
 * version 2.0 (the "License"). You can obtain a copy of the License at
 * http://mozilla.org/MPL/2.0/.
 */

/*
 * This is similar to the [JavaScript Shell](<http://www.squarefree.com/shell/>)
 * (or as available in [Komodo Developer
 * Extension](http://community.activestate.com/xpi/komodo-developer-extension))
 * or the [JavaScript Environment](<https://www.squarefree.com/jsenv/>)
 * bookmarklets, but lets you use the power of the Komodo editor to modify the
 * code.
 *
 * Additionally, line numbers should work for both errors and print statements
 * (and are integrated into the command output tab).
 *
 * There are three special global functions in the context: print, props and
 * clear:
 *  print(aString)
 *    Displays aString with the line number of the print statement.
 *  props(aObject)
 *    Displays the properties of an object and the inheritance chain.
 *  clear()
 *    Removes all statements printed to the command window.
 *
 * Author: Patrick Cloke <clokep@gmail.com>
 * URL: https://bitbucket.org/clokep/komodo-tools
 * Version: 0.1
 * Last Updated: 2012-05-07 0834
 */

let Ci = Components.interfaces;
let scimoz = ko.views.manager.currentView.scimoz;
// Get the current document we're running on.
let currentDoc = ko.views.manager.currentView.koDoc;
let output = ko.run.output;

function start() {
  // The output should be of the form: "<line number>: <message>".
  const outputParser = "^(?P<line>\\d+): (?P<content>.*)$";

  // Open the output session with some nice names, clearing the content window
  // on open.
  let filename = currentDoc.baseName;
  let file = currentDoc.displayPath.file;
  let path = file ? file.dirName : "";
  output.startSession(filename, true, outputParser, path, filename, true);
}
start();
// Ensure the tab is showing.
output.show();

// Get the output terminal to use.
let term = output.getTerminal().QueryInterface(Ci.koITreeOutputHandler);

// Define some nice functions to use when debugging, note that these are an
// attempt to emulate the JavaScript Shell.
let hasPrinted = false;
function print(aString) {
  let lineNumber = Components.stack.caller.lineNumber + offset;
  let string = (hasPrinted ? "\n" : "") + lineNumber + ": " + aString;
  term.proxyAddText(string.length, string, "<stdout>");
  hasPrinted = true;
}
function clear() {
  // Close the current session and start a new one, term.clear() doesn't seem to
  // work.
  term.endSession(0);
  start();
}
/*
 * This function is based on the JavaScript Shell bookmarklet:
 * [http://www.squarefree.com/shell/]. Available as MPl 1.1/GPL/LGPL
 * tri-license.
 */
function props(aObject) {
  if (aObject === null) {
    error("props called with null argument");
    return;
  }

  if (aObject === undefined) {
    error("props called with undefined argument");
    return;
  }

  let output = "";

  // The output object.
  let as = {"Methods": [], "Fields": [], "Unreachables": []};
  let p, j, i; // loop variables, several used multiple times

  // For each __proto__, add an empty array for each namespace.
  let protoLevels = 0;
  for (p = aObject; p; p = p.__proto__) {
    //for (i = 0; i < ns.length; ++i)
    for (i in as)
      as[i][protoLevels] = [];
    ++protoLevels;
  }

  // Iterate over each property of an object.
  for (let a in aObject) {
    // Shortcoming: doesn't check that VALUES are the same in object and
    // prototype.

    // Find the level that this property comes from.
    let protoLevel = -1;
    try {
      for (p = aObject; p && (a in p); p = p.__proto__)
        ++protoLevel;
    } catch(er) {
      // "in" operator throws when param to props() is a string
      protoLevel = 0;
    }

    let type = "Fields";
    try {
      if ((typeof aObject[a]) == "function")
        type = "Methods";
    } catch (er) {
      type = "Unreachables";
    }

    // Add the current property as the correct type to it's  __proto__ level.
    as[type][protoLevel].push(a);
  }

  function times(s, n) (n ? s + times(s, n-1) : "");

  // For each prototype level, print out each type of property that exists.
  for (j = 0; j < protoLevels; ++j) {
    for (i in as) {
      if (as[i][j].length) {
        output += i + times(" of prototype", j) + ": " +
                  as[i][j].sort().join(", ") + "\n";
      }
    }
  }

  // Display the output.
  print(output.slice(0, -1));
}

// Get the selected text from the current document, if no text is selected, then
// use the whole document. If text is selected, account for this offset in line
// numbers.
let text = scimoz.selText;
let offset = 1;
if (!text.length)
  text = scimoz.text;
else
  offset += scimoz.lineFromPosition(Math.min(scimoz.anchor, scimoz.currentPos));

let exitState = 0;
try {
  // Evaluate the document in an empty sandbox (except for the functions we want
  // added!).
  let sandbox = Components.utils.Sandbox("about:blank");
  sandbox.print = print;
  sandbox.clear = clear;
  sandbox.props = props;
  // Evaluate in the sandbox, using JavaScript version 1.8, the current path
  // name and consider the first line to be the offset.
  // TODO automatically get the highest JavaScript version available.
  Components.utils.evalInSandbox(text, sandbox, "1.8", currentDoc.displayPath,
                                 offset);
} catch (e) {
  let string = (hasPrinted ? "\n" : "") + e.lineNumber + ": " + e.toString();
  term.proxyAddText(string.length, string, "<stderr>");
  hasPrinted = true;
  exitState = 1;
}

output.endSession(exitState);
