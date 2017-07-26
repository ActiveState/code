// Highlight the word under the cursor.
var scimoz = ko.views.manager.currentView.scimoz;
var start = scimoz.wordStartPosition(scimoz.currentPos, true);
var end = scimoz.wordEndPosition(scimoz.currentPos, true);
scimoz.anchor = start;
scimoz.currentPos = end;
