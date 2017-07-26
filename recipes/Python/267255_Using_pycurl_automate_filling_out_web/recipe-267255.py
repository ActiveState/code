import xml.sax
import urllib
import urlparse
import pycurl
import StringIO
import os

# Requires pycurl - the Python bindings to libcurl. http://pycurl.sourceforge.net/
# Also requires libcurl - the automated web browsing library http://curl.haxx.se/

path_to_OPML = r'C:\Program Files\amphetadesk-win-v0.93.1\data\myChannels.opml'
# The url of the Drupal "New feed" page is usually something like
# http://mysite.com/admin/node/syndication/news/add/feed
scheme = 'http'
host = 'my_site.com'
login_path = '/user/login'
login_dest_path = '/blog'
add_feed_path = '/admin/node/syndication/news/add/feed'
user = 'me'
password = ''
login_url = urlparse.urlunsplit((scheme, host, login_path, '', ''))
login_dest_url = urlparse.urlunsplit((scheme, host, login_dest_path, '', ''))
add_feed_url = urlparse.urlunsplit((scheme, host, add_feed_path, '', ''))
show_output = True

# Drupal uses pass-through authentication, not HTTP authentication
# This means we fill out the login form instead of using
# urllib2.HTTPBasicAuthHandler.  Cookie support is not native in
# the Python client libraries.  There is a (beta) ClientCookie module
# which purports to manage cookies.

# Instead, I'm using pycurl, the Python bindings to libcurl.  libcurl
# is a rich http & ftp client with native support for cookies.

# What we want to do is mimic the behavior of the login form
# and send the data to the server using HTTP POST.  Then we get the
# PHPSESSID cookie sent back from Drupal and store it so we can send
# it with the add feed requests.

# XML Parsing event handlers.  We use event-driven XML parsing with
# SAX.  In this style every time a tag is encountered in the parser's traversal
# of the document, an event is raised and a callback function (handler) is called.

class OPML_Uploader(xml.sax.ContentHandler):
    def startDocument(self):
        # Called when XML (OPML) document starts.  Here we
        # set up curl and log in to the site.

        # Buffers
        self.file1 = StringIO.StringIO()
        self.file2 = StringIO.StringIO()

        # A string with the name and path of an appropriate temp file
        # (varies by platform)
        cookie_file_name = os.tempnam()

        # Handle to libcurl object
        self.crl = pycurl.Curl()

        # URL encodings of form data
        login_form_seq = [
            ('edit[destination]', login_dest_url),
            ('edit[name]', user),
            ('edit[pass]', password),
            ('edit[remember_me]', '0'),
            ('op', 'Log in')]
        login_form_data = urllib.urlencode(login_form_seq)

        # Set libcurl options.  Commented with their equivalent
        # curl command line options.  These options are "sticky".

        # Option -L  Follow  "Location: "  hints
        self.crl.setopt(pycurl.FOLLOWLOCATION, 1)

        # Option -b/--cookie <name=string/file> Cookie string or file to read cookies from
        # Note: must be a string, not a file object.
        self.crl.setopt(pycurl.COOKIEFILE, cookie_file_name)

        # Option -c/--cookie-jar <file> Write cookies to this file after operation
        # Note: must be a string, not a file object.
        self.crl.setopt(pycurl.COOKIEJAR, cookie_file_name)

        # Option -d/--data <data>   HTTP POST data
        self.crl.setopt(pycurl.POSTFIELDS, login_form_data)
        self.crl.setopt(pycurl.URL, login_url)
        if show_output:
            self.crl.setopt(pycurl.WRITEFUNCTION, self.file1.write)
        self.crl.perform()
        if show_output:
            print self.crl.getinfo(pycurl.HTTP_CODE), self.crl.getinfo(pycurl.EFFECTIVE_URL)

    def startElement(self, tag, attributes):
        # Called at the start of each tag.  Here we add the feed to
        # Drupal syndication.
        if show_output:
            print tag

        if tag != 'outline':
            return

        # Insert form data elements based on the attributes
        # in the OPML node.
        add_feed_form_seq = [
            ('edit[title]', '~ FEED TITLE GOES HERE ~'),
            ('edit[url]', '~ URL TO FEED GOES HERE ~'),
            ('edit[attributes]', ''),
            ('edit[refresh]', '3600'),
            ('op', 'Submit')]
        add_feed_form_seq[0] = ('edit[title]', attributes.get('title'))
        add_feed_form_seq[1] = ('edit[url]', attributes.get('xmlurl'))
        add_feed_form_data = urllib.urlencode(add_feed_form_seq)

        # Set up for "add feed" form
        self.crl.setopt(pycurl.POSTFIELDS, add_feed_form_data)
        self.crl.setopt(pycurl.URL, add_feed_url)
        if show_output:
            self.crl.setopt(pycurl.WRITEFUNCTION, self.file2.write)
        self.crl.perform()
        if show_output:
            print self.crl.getinfo(pycurl.HTTP_CODE), self.crl.getinfo(pycurl.EFFECTIVE_URL)

    def _close_out_curl(self):
        self.crl.close()
        if show_output:
            print self.file1.getvalue()
            print self.file2.getvalue()

# New instance of the handler object
my_handler = OPML_Uploader()

# Parse the OPML and make the new feeds in Drupal
xml.sax.parse(path_to_OPML, my_handler)
