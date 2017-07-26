import sys
import os
import unittest
import tempfile
import stat
import re

def _write(path, content):
    f = open(path, 'w')
    try:
        f.write(content)
    finally:
        f.close()

def _run(cmd):
    if sys.platform == "win32":
        redirect = " >nul 2>&1"
    else:
        redirect = " >/dev/null 2>&1"
    retval = os.system(cmd+redirect)
    if retval:
        raise OSError("error running '%s': retval=%r"
                      % (cmd+redirect, retval))

class CopyTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing.
        self.tmpdir = tempfile.mktemp()
        os.mkdir(self.tmpdir)
        os.chdir(self.tmpdir)

    def tearDown(self):
        # Clean up temporary directory.
        if sys.platform.startswith("win"):
            _run('attrib -R /s "%s"' % self.tmpdir)
            _run('rd /s/q "%s"' % self.tmpdir)
        else:
            _run('chmod -R 0777 "%s"' % self.tmpdir)
            _run('rm -rf "%s"' % self.tmpdir)

    def assertRaisesEx(self, exception, callable, *args, **kwargs):
        if "exc_args" in kwargs:
            exc_args = kwargs["exc_args"]
            del kwargs["exc_args"]
        else:
            exc_args = None
        if "exc_pattern" in kwargs:
            exc_pattern = kwargs["exc_pattern"]
            del kwargs["exc_pattern"]
        else:
            exc_pattern = None

        argv = [repr(a) for a in args]\
               + ["%s=%r" % (k,v)  for k,v in kwargs.items()]
        callsig = "%s(%s)" % (callable.__name__, ", ".join(argv))

        try:
            callable(*args, **kwargs)
        except exception, exc:
            if exc_args is not None:
                self.failIf(exc.args != exc_args,
                            "%s raised %s with unexpected args: "\
                            "expected=%r, actual=%r"\
                            % (callsig, exc.__class__, exc_args, exc.args))
            if exc_pattern is not None:
                self.failUnless(exc_pattern.search(str(exc)),
                                "%s raised %s, but the exception "\
                                "does not match '%s': %r"\
                                % (callsig, exc.__class__, exc_pattern.pattern,
                                   str(exc)))
        except:
            exc_info = sys.exc_info()
            print exc_info
            self.fail("%s raised an unexpected exception type: "\
                      "expected=%s, actual=%s"\
                      % (callsig, exception, exc_info[0]))
        else:
            self.fail("%s did not raise %s" % (callsig, exception))

    def test_copy(self):
        import shutil
        _write("foo", content="this is foo")
        _write("noaccess", content="you don't have write permissions for me")
        os.chmod("noaccess", 0444)
        #self.assertRaises(OSError, shutil.copy, "foo", "noaccess")
        #self.assertRaisesEx(OSError, shutil.copy, "foo", "noaccess")
        #self.assertRaisesEx(IOError, shutil.copy, "foo", "noaccess",
        #                    exc_args=(14, "Permission denied"))
        #self.assertRaisesEx(IOError, shutil.copy, "foo", "noaccess",
        #                    exc_pattern=re.compile("Permission denied"))
        self.assertRaisesEx(IOError, shutil.copy, "foo", "noaccess",
                            exc_pattern=re.compile("No such file or directory"))

if __name__ == "__main__":
    argv = sys.argv[:]
    argv.insert(1, "-v") # make output verbose by default
    unittest.main(argv=argv)
