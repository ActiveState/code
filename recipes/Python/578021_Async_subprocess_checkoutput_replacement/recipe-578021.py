# -*- coding: utf-8 -*-
from twisted.internet.defer import Deferred
from twisted.internet.error import ProcessDone
from twisted.internet.protocol import ProcessProtocol

class SubprocessProtocol(ProcessProtocol):
    outBuffer = ""
    errBuffer = ""

    def connectionMade(self):
        self.d = Deferred()

    def outReceived(self, data):
        self.outBuffer += data

    def errReceived(self, data):
        self.errBuffer += data

    def processEnded(self, reason):
        if reason.check(ProcessDone):
            self.d.callback(self.outBuffer)
        else:
            self.d.errback(reason)

def async_check_output(args, ireactorprocess=None):
    """
    :type args: list of str
    :type ireactorprocess: :class: twisted.internet.interfaces.IReactorProcess
    :rtype: Deferred
    """
    if ireactorprocess is None:
        from twisted.internet import reactor
        ireactorprocess = reactor

    pprotocol = SubprocessProtocol()
    ireactorprocess.spawnProcess(pprotocol, args[0], args)
    return pprotocol.d

# actual code ends here, unit tests follow and may be omitted or saved in separate file, don't forget to remove appropriate
# comments 
# -*- coding: utf-8 -*-
from twisted.internet.error import ProcessTerminated

from twisted.trial.unittest import TestCase
from twisted.internet.defer import inlineCallbacks
#from twisted_subprocess import async_check_output


class TestSpawning(TestCase):

    @inlineCallbacks
    def test_check_output_returns_command_output_if_success(self):
        self.assertEquals("hello world", (yield async_check_output(["echo", "hello world"])).strip())

    def test_check_output_calls_errback_if_exit_status_not_zero(self):
        return self.assertFailure(async_check_output(["false"]), ProcessTerminated)

    def test_check_output_returns_errback_if_nonexisting_executable(self):
        return self.assertFailure(async_check_output(["sdfsdfdsf329909092"]), ProcessTerminated)
