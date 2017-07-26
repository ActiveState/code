// For Komodo 6
if (ko.views.manager.currentView &&
    ko.views.manager.currentView.scimoz) {
    // Set the number of completions shown in the list.
    ko.views.manager.currentView.scimoz.autoCMaxHeight = 10;
}

// For Komodo 7
if (ko.prefs) {
  ko.prefs.setLongPref("codeintel_autocomplete_max_rows", 10);
}
