if (typeof(window.extensions) == 'undefined') {
    window.extensions = {};
}
if (typeof(window.extensions.resetFocus) == 'undefined') {
    window.extensions.resetFocus = {
        observe: function(subject, topic, data) {
            if (topic == "application-activated") {
                if (ko.views.manager.currentView) {
                    ko.views.manager.currentView.setFocus();
                }
            }
        }
    };

    var observerSvc = Components.classes["@mozilla.org/observer-service;1"].
                    getService(Components.interfaces.nsIObserverService);
    observerSvc.addObserver(window.extensions.resetFocus,
                            "application-activated", false);
}
