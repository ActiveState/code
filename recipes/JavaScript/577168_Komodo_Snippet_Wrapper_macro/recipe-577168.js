var view = ko.views.manager.currentView;
var scimoz = view.scimoz;

var snippet_name = ko.dialogs.prompt('Enter a wrapper snippet name');

if (snippet_name && snippet_name.length > 0) {
  var snpt = ko.abbrev.findAbbrevSnippet(snippet_name);

  if (!/\[\[%(s|w|S|W)\]\]/.test(snpt.value)) {
    ko.dialogs.alert('FAIL: no selection / word under cursor interpolation in this snippet! Are you sure this is is a \'wrapper snippet\'?');
  } else {
    ko.abbrev.insertAbbrevSnippet(snpt);
  }
}
