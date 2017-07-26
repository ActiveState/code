class Strsignal:
    """An instance of this class emulates the standard (POSIX.1-2008)
       C library function strsignal().  If possible, it calls the real
       C library function, using ctypes; if this is not possible, it
       produces the name of the SIGxxx constant (from the signal
       module) corresponding to the signal number passed in; if *that*
       doesn't work either, it returns the string "signal %d" with the
       %d replaced with the decimal signal number.

       For testing purposes, functions that implement a single one of
       the strategies above can be retrieved from the static methods
       get_ctypes_strsignal, get_reversemap_strsignal, and
       get_fallback_strsignal.  These methods may throw arbitrary
       exceptions.
    """

    def __init__(self):
        """Which strategy we will use is lazily determined on the first call."""
        self._strsignal = None

    def __call__(self, signo):
        """External entry point."""
        if self._strsignal is None:
            self.lazy_init()
        return self._strsignal(signo)

    def lazy_init(self):
        """Pick whichever of our three strategies doesn't throw an exception
           upon instantiation."""
        try:
            self._strsignal = self.get_ctypes_strsignal()
        except:
            try:
                self._strsignal = self.get_reversemap_strsignal()
            except:
                self._strsignal = self.get_fallback_strsignal()

    @staticmethod
    def get_ctypes_strsignal():
        """Strategy 1: If the C library exposes strsignal(), use it."""
        import signal
        import ctypes
        import ctypes.util
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        strsignal_proto = ctypes.CFUNCTYPE(ctypes.c_char_p,
                                           ctypes.c_int)
        strsignal_c = strsignal_proto(("strsignal", libc), ((1,),))
        NSIG = signal.NSIG
        def strsignal_ctypes_wrapper(signo):
            # The behavior of the C library strsignal() is unspecified if
            # called with an out-of-range argument.  Range-check on entry
            # _and_ NULL-check on exit.
            if 0 <= signo < NSIG:
                s = strsignal_c(signo)
                if s:
                    return s.decode("utf-8")
            return "Unknown signal "+str(signo)

        return strsignal_ctypes_wrapper

    @staticmethod
    def get_reversemap_strsignal():
        """Strategy 2: return the name of the signal constant corresponding to
           the value passed in."""
        import signal

        signames = [None] * signal.NSIG
        for constant in dir(signal):
            if not constant.startswith("SIG"):
                continue
            if constant.startswith("SIG_"):
                continue
            # obsolete names for signals
            if constant in ('SIGIOT', 'SIGCLD', 'SIGPOLL'):
                continue
            signames[getattr(signal, constant)] = constant

        for rt in range(signal.SIGRTMIN+1, signal.SIGRTMAX):
            signames[rt] = "SIGRTMIN+"+str(rt - signal.SIGRTMIN)

        for gap in range(len(signames)):
            if signames[gap] is None:
                signames[gap] = "SIG_"+str(gap)

        NSIG = signal.NSIG
        def strsignal_reversemap_wrapper(signo):
            if 0 <= signo < NSIG:
                return signames[signo]
            else:
                return "Unknown signal "+str(signo)

        return strsignal_reversemap_wrapper

    @staticmethod
    def get_fallback_strsignal():
        """Strategy F: just return "signal N" where N is the signal
           number."""

        def strsignal_fallback_wrapper(signo):
            return "signal "+str(signo)

        return strsignal_fallback_wrapper

strsignal = Strsignal()
__all__ = ('strsignal',)

if __name__ == '__main__':

    def main():
        import signal
        import sys
        import traceback

        try:
            strsignal_c = Strsignal.get_ctypes_strsignal()
        except Exception as e:
            sys.stdout.write("Ctypes strsignal unavailable: ")
            sys.stdout.write(traceback.format_exception_only(type(e), e)[0])
            strsignal_c = lambda _: "--"

        try:
            strsignal_r = Strsignal.get_reversemap_strsignal()
        except Exception as e:
            sys.stdout.write("Reverse-map strsignal unavailable: ")
            sys.stdout.write(traceback.format_exception_only(type(e), e)[0])
            strsignal_r = lambda _: "--"

        try:
            strsignal_f = Strsignal.get_fallback_strsignal()
        except Exception as e:
            sys.stdout.write("Fallback strsignal unavailable: ")
            sys.stdout.write(traceback.format_exception_only(type(e), e)[0])
            strsignal_f = lambda _: "--"

        try:
            strsignal(1)
            strsignal(0)
            strsignal(-9999)
            strsignal_a = strsignal
        except:
            sys.stdout.write("Automatic strsignal unavailable: ")
            traceback.print_exc(limit=0, file=sys.stdout)
            strsignal_a = lambda _: "--"

        rows = [('N', 'Auto', 'Ctypes', 'Revmap', 'Fallback')]
        for n in [-signal.NSIG-1, -1] + list(range(signal.NSIG + 2)):
            rows.append((str(n),
                         strsignal_a(n),
                         strsignal_c(n),
                         strsignal_r(n),
                         strsignal_f(n)))

        cols = zip(*rows)
        col_widths = [ max(len(val) for val in col) for col in cols ]
        form = '  '.join(['{{:<{0}}}'.format(width) for width in col_widths])
        form += '\n'

        for row in rows:
            sys.stdout.write(form.format(*row))

    main()
