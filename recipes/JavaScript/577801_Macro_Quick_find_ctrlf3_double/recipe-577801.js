/**
 *
 * Original:
 * Copyright (c) 2009 Stan Angeloff http://blog.angeloff.name
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

if (typeof (extensions) === 'undefined')
        window.extensions = {};

(function() {

        const Cc = Components.classes;
        const Ci = Components.interfaces;

        // Get a reference to the script namespace
        var $self = extensions.findWordUnderCursor ||
                                (extensions.findWordUnderCursor = { events: {} });

        // Clean-up after previous execution
        if ($self.onViewClosed)
                window.removeEventListener('view_closed', $self.onViewClosed, false);
        if ($self.onViewOpened)
                window.removeEventListener('view_opened', $self.onViewOpened, false);
        if ($self.destroyAll)
                $self.destroyAll();

        $self.isSupportedView = function(view) {

                return (view && view.getAttribute('type') === 'editor');
        };

        $self.onViewOpened = function(e) {

                var view = e.originalTarget;

                if ($self.isSupportedView(view))
                        $self.apply(view);
        };

        $self.onViewClosed = function(e) {

                var view = e.originalTarget;

                if ($self.isSupportedView(view))
                        $self.destroy(view);
        };

        $self.destroy = function(view) {

                if (view.uid in $self.events) {

                        view.removeEventListener('dblclick', $self.events[view.uid], false);

                        delete $self.events[view.uid];
                }
        };

        $self.apply = function(view) {

                var fn = function(e) {

                        if (e.which === 1 &&
                                ! (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) &&
                                ! (view.scimoz._startDragDrop || view.scimoz._inDragDrop)) {

                                e.stopPropagation();
                                e.preventDefault();

                                $self.jumpToSearch(view);
                        }
                };

                //view.addEventListener('mouseup', fn, false);
                dblclick:view.addEventListener('dblclick', fn, false);

                $self.events[view.uid] = fn;
        };

        window.addEventListener('view_opened', $self.onViewOpened, false);
        window.addEventListener('view_closed', $self.onViewClosed, false);

        $self.forEach = function(fn) {

                var viewsByType = ko.views.manager.topView.getViewsByType(true, 'editor'),
                        view;

                for (var i = 0; i < viewsByType.length; i ++) {

                        view = viewsByType[i];

                        if ($self.isSupportedView(view))
                                fn.apply($self, [view]);
                }
        };

        $self.applyToAll = function() { $self.forEach($self.apply); };
        $self.destroyAll = function() { $self.forEach($self.destroy); };

        $self.jumpToSearch = function(view) {
            startLine = ko.views.manager.currentView.scimoz.firstVisibleLine;
            ko.commands.doCommand("cmd_findNextSelected");
            ko.commands.doCommand("cmd_findPrevious");
            endLine = ko.views.manager.currentView.scimoz.firstVisibleLine;
            changeLine = startLine - endLine;
            
            //in case it jumps to the top then back in the event that the next
            //selected is at the top of the screen.
            ko.views.manager.currentView.scimoz.lineScroll(0, changeLine);
            
        };

        $self.applyToAll();

})();
