var view = ko.views.manager.currentView;
var scimoz = view.scimoz;
var currentWord = ko.interpolate.getWordUnderCursor(scimoz);
if (currentWord) {
    var snippetText = '[[%tabstop1:"]][[%w]][[%tabstop1]]';
    var langName = view.languageObj.name.toLowerCase();
    if (langName.indexOf("html") >= 0 ||
        langName.indexOf("xml") >= 0) {
        // Add tags around the text.
        snippetText = '<[[%tabstop1:div]]>[[%w]]</[[%tabstop1]]>';
    }
    var fakeSnippet = {
            hasAttribute: function(name) {
                    return name in this;
            },
            getStringAttribute: function(name) {
                    return this[name];
            },
            name: "autowrap snippet",
            indent_relative: "true",
            value: snippetText
    };
    ko.projects.snippetInsert(fakeSnippet);
} else {
    ko.statusBar.AddMessage("Nothing under the cursor to wrap.", "editor", 5000, true);
}
