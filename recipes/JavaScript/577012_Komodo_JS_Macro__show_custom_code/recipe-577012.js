/**
 * @type {Components.interfaces.ISciMoz}
 */
var scimoz = ko.views.manager.currentView.scimoz;
var sep = String.fromCharCode(scimoz.autoCSeparator);
var completions = ["item1", "item2"];
scimoz.autoCShow(0, completions.join(sep));
