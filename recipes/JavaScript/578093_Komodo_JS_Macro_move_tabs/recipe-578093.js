// Get the XUL tabbox element (it contains XUL *tabs* and *tabpanels* elements).
// Note: This may not work correctly for Komodo split views.
var tabbox = document.getElementById("tabbed-view");
var tabs = tabbox.tabs;
// Move the tab to the start.
tabs.insertBefore(tabs.selectedItem, tabs.firstChild);
// Ensure it's visible.
tabs.scrollBoxObject.ensureElementIsVisible(tabs.firstChild);
