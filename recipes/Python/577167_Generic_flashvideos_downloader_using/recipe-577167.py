#!/usr/bin/python
"""
Log resources requested by a webpage using WebKit.

Originally designed to download video files requested by Adobe Flash videos.
"""   
import sys
import re

# Third-party modules
import webkit
import gtk

# Supported sites (key: URL regexp, value: video URL regexp)
SITES = {
    "youtube\.com/": "youtube\.com/videoplayback",
    "blip\.tv/": "blip\.tv/file/get/",
}

def debug(line):
    """Write debug line to standard error."""
    sys.stderr.write("--- %s\n" % line)

def first(it):
    """Return first element in iterator (None if empty)."""
    return next(it, None)

def on_request(view, frame, resource, request, response, 
               resource_regexp, skip_regexp=None):
    """Check if requested resource matches the video resource_regexp regexp."""
    url = request.get_uri()
    message = request.get_property("message")
    if not message:
        return
    method = message.get_property("method")
    if skip_regexp and skip_regexp.search(url):
        # cancel the request
        request.set_uri("about:blank")
        return
    debug("request: %s %s" % (method, url))
    if resource_regexp and re.search(resource_regexp, url):
        debug("videofile match: %s" % url)
        print url
        gtk.main_quit()

def create_webview():
    """Create a gtk.Window containing a WebKit webview."""
    view = webkit.WebView()
    window = gtk.Window()
    scrolled = gtk.ScrolledWindow()
    scrolled.add(view)
    window.add(scrolled)
    return window, view
 
def main(args):
    import optparse
    usage = """usage: %%prog [Options]\n\n%s""" % __doc__.strip()
    parser = optparse.OptionParser(usage)
    parser.add_option('-t', '--test', dest='test', action="store_true", 
                      default=False, help="Run in test mode (show webview)")
    options, args0 = parser.parse_args(args)    
    url, = args0
    resource_regexp = first(pattern for (urlre, pattern) in SITES.iteritems() 
                       if re.search(urlre, url))    
    if not resource_regexp and not options.test:
        debug("No module found for URL: %s" % url)
        return 1
    window, webview = create_webview()
    skip_regexp = re.compile(r"\.(jpg|png|gif|css)(\?|$)", re.I)
    webview.connect("resource-request-starting", on_request, resource_regexp, skip_regexp)
    webview.load_uri(url)    
    if options.test:
        window.resize(640, 480)
        window.show_all()        
    gtk.main()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
