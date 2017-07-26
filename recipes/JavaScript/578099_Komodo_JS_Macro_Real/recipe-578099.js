if (typeof (mymacros) == "undefined") {
  mymacros = {};
  mymacros.started = false;
  mymacros.autoReflow = function (event) {
    // stop if using Undo/Redo - it will not function properly
    var ch = (String.fromCharCode(event.charCode)).toLowerCase();
    if (event.ctrlKey && (ch == 'z' || ch == 'y'))
      return;
    
    var scimoz = ko.views.manager.currentView.scimoz;
    if (scimoz.getColumn(scimoz.currentPos) > 79) {
      ko.commands.doCommand("cmd_editReflow");
    }
  } 
}

if (!mymacros.started) {
  mymacros.started = true;
  window.addEventListener("keypress", mymacros.autoReflow, true);
}
else {
  mymacros.started = false;
  window.removeEventListener("keypress", mymacros.autoReflow, true);
}
