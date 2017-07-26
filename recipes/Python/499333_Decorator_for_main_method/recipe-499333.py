import getopt,sys,traceback
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __repr__(self):
        return self.msg

def main_function(getOptString='', numArgs=0):
    def main_decorator(maincode):
        def decorated_main(argv=[__name__]):
            try:
                opts={}
                args=[]
                if len(getOptString) > 0:
                    try:
                        opt_list, args = getopt.getopt(argv[1:], getOptString)
                        opts=dict([(x[0][1:], x[1]) for x in opt_list])
                    except getopt.error, msg:
                        raise Usage(msg)
                else:
                    args=argv[1:]
                if len(args) < numArgs:
                    raise Usage("Not enough arguments")
                return maincode(args, opts) or 0
            except KeyboardInterrupt:
                sys.exit(-1)
            except SystemExit:
                pass
            except Usage, usage:
                sys.stderr.write('%s\n%s\n' % (maincode.__doc__, usage.msg))
            except Exception, err:
                cla, exc, trbk = sys.exc_info()
                import traceback
                sys.stderr.write("Caught Exception:\n%s:%s\n%s" % (cla.__name__, str(exc), ''.join(traceback.format_tb(trbk,5))))
                sys.exit(-1)
        return decorated_main
    return main_decorator

########### Example Usage ################

@main_function('o:', 2)
def main(args, opts):
    """Usage: test.py [-o opt1] arg1 arg2"""

if __name__=="__main__":
    sys.exit(main(sys.argv) or 0)
