#!/usr/bin/python
import logging
try:
    import webapp2
except:
    logging.exception("no webapp")
import pprint
import os
import StringIO
os.environ["MATPLOTLIBDATA"] = os.getcwdu()
os.environ["MPLCONFIGDIR"] = os.getcwdu()
import subprocess
def no_popen(*args, **kwargs): raise OSError("forbjudet")
subprocess.Popen = no_popen
subprocess.PIPE = None
subprocess.STDOUT = None
logging.warn("E: %s" % pprint.pformat(os.environ))
try:
    import numpy, matplotlib, matplotlib.pyplot as plt
except:
    logging.exception("trouble")

def dynamic_png():
    try:
        plt.title("Dynamic PNG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="png")
        plt.clf()
        return """<img src="data:image/png;base64,%s"/>""" % rv.getvalue().encode("base64").strip()
    finally:
        plt.clf()

def dynamic_svg():
    try:
        plt.title("Dynamic SVG")
        for i in range(5): plt.plot(sorted(numpy.random.randn(25)))
        rv = StringIO.StringIO()
        plt.savefig(rv, format="svg")
        return rv.getvalue()
    finally:
        plt.clf()

if __name__ == "__main__":
    print dynamic_png()
    print dynamic_svg()
else:
    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write("""<html><head/><body>""")
            self.response.write(dynamic_png())
            self.response.write(dynamic_svg())
            self.response.write("""</body> </html>""")

    app = webapp2.WSGIApplication([
        ('/', MainHandler)
    ], debug=True)
