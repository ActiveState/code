# In the public domain
# Author: Andrew Dalke <dalke@dalkescientific.com
#
# This is an example of a wxPython-based modal progress bar
# which uses Twisted to do XML-RPC requests from the state name
# demo server.  It's easily extensible to other tasks.

from __future__ import generators
from wxPython.wx import *

from twisted.internet import reactor
from twisted.web.xmlrpc import Proxy

# returned from the main modal
COMPLETED, CANCELED, ERROR = range(3)

# returned from the (sub)modal when there's an XML-RPC error
RETRY, SKIP, STOP = range(20, 23)

# The progress modal does N "tasks".  Each task has a 
# "start" method, which returns a deferred.  The deferred
# is chained to call "good" with the result or "bad"
# with the failure.  The "bad" method may return one of
# RETRY, SKIP, or STOP to tell the modal how to recover.
class Task:
    def start(self):
        """returns a defered"""
        raise NotImplementedError
    def good(self, result):
        pass
    def bad(self, fail):
        pass

# To show examples of error modes
TEST_ERRORS = 1

# A Task to get the state name corresponding to the given number.
class StateTask(Task):
    def __init__(self, i):
        self.i = i

    def start(self):
        proxy = Proxy("http://beatty.userland.com/RPC2")
        if TEST_ERRORS:
            i = self.i
            if i == 3:
                proxy = Proxy("http://illegal-host_name/")
            elif i == 6:
                proxy = Proxy("http://beatty.userland.com/")
            elif i == 8:
                proxy = Proxy("http://beatty.userland.com/testing_xmlrpc_error_case")
            
        return proxy.callRemote('examples.getStateName', self.i)

    def good(self, result):
        print "state", self.i, "is", result

    def bad(self, fail):
        # pop up a submodal
        status = wxMessageBox("Cannot get name for state %d.  Try again?\n"
                              "\n"
                              "The problem is: %s" % (self.i, fail.getErrorMessage()),
                              "Connection problem",
                              wxCANCEL | wxYES_NO | wxICON_QUESTION)
        if status == wxYES:
            return RETRY
        elif status == wxNO:
            return SKIP
        elif status == wxCANCEL:
            return STOP
        else:
            raise AssertionError(status)

# The progress dialog must be passed a "task list" object which
# implements len() (needed to know how many steps to show) and
# does forward iteration.
class StateTaskList:
    def __init__(self, min=0, max=50):
        self.min = min
        self.max = max
    def __iter__(self):
        for i in range(self.min, self.max):
            yield StateTask(i)
            
    def __len__(self):
        return self.max - self.min
        

class Progress(wxDialog):
    def __init__(self, parent, ID, title, tasks,
                 pos=wxDefaultPosition, size=wxDefaultSize,
                 style=wxDEFAULT_DIALOG_STYLE):
        wxDialog.__init__(self, parent, ID, title, pos, size, style)

        n = len(tasks)
        self.task_iter = iter(tasks)

        sizer = wxBoxSizer(wxVERTICAL)

        self.gauge = wxGauge(self, -1, 100, size = (300, -1))
        sizer.Add(self.gauge, 0, wxALIGN_CENTER|wxALL, 5)

        box = wxBoxSizer(wxHORIZONTAL)
        spacer = wxStaticText(self, -1, "")
        box.Add(spacer, 1, wxALIGN_CENTRE|wxALL|wxGROW)
        btn = wxButton(self, wxID_CANCEL, " Cancel ")
        box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
        spacer = wxStaticText(self, -1, "")
        box.Add(spacer, 1, wxALIGN_CENTRE|wxALL|wxGROW)

        sizer.AddSizer(box, 0, wxALIGN_CENTER_VERTICAL|wxALL|wxGROW, 5)

        EVT_BUTTON(self, wxID_CANCEL, self.OnCancel)

        self.SetSizer(sizer)
        self.SetAutoLayout(true)
        sizer.Fit(self)

        self.i = 0
        self.Start(n)

        self._canceled = 0
        self.Feed()

    def OnCancel(self, event):
        self._canceled = 1
        self.EndModal(CANCELED)

    def Feed(self):
        # Get the next task and start it up
        try:
            task = self.task_iter.next()
        except StopIteration:
            self.End()
            return
        self.StartTask(task)

    def StartTask(self, task):
        defered = task.start()
        def do_good(result):
            self.Good(task, result)
        def do_bad(fail):
            self.Bad(task, fail)
        defered.addCallbacks(do_good, do_bad)

    def Good(self, task, result):
        if self._canceled:
            return
        task.good(result)
        self.Update(1)
        self.Feed()

    def Bad(self, task, fail):
        if self._canceled:
            return
        try_again = task.bad(fail)
        if try_again == RETRY:
            self.StartTask(task)
        elif try_again == SKIP:
            self.Update(1)
            self.Feed()
        elif try_again == STOP:
            self._canceled = 1
            self.EndModal(ERROR)
        else:
            raise AssertionError(try_again)

    def Start(self, count):
        self.gauge.SetRange(count)
        self.gauge.SetValue(0)

    def Update(self, incr):
        # Increment the counter.
        self.i += incr
        self.gauge.SetValue(self.i)
        
    def End(self):
        self.gauge.SetValue(self.gauge.GetRange())
        self.EndModal(COMPLETED)

# Thanks to Uwe C. Schroeder and his "Using wxPython with Twisted
# Python" recipe at aspn.ActiveState.com

class MyApp(wxApp):
    def OnInit(self):
        # Twisted Reactor code
        reactor.startRunning()
        EVT_TIMER(self, 999999, self.OnTimer)
        self.timer = wxTimer(self, 999999)
        self.timer.Start(150, False)

        return true

    def OnTimer(self, event):
        reactor.runUntilCurrent()
        reactor.doIteration(0)

    def __del__(self):
        self.timer.Stop()
        reactor.stop()
        wxApp.__del__(self)

def main():
    app = MyApp(0)
    win = Progress(None, -1, "Processing ...", StateTaskList(1, 10))

    status = win.ShowModal()
    if status == COMPLETED:
        print "All done"
    elif status == CANCELED:
        print "Okay, I stopped."
    elif status == ERROR:
        print "What happened?"
    else:
        raise AssertionError(status)
    
if __name__ == "__main__":
    main()
