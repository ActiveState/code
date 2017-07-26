import urllib.request
import urllib.parse
import getpass

class CosignPasswordMgr(object):
    """A password manager for CosignHandler objects.

    """

    def newcred(self):
        """Default callback.

        Ask user for username and password."""
        return {'login': input('username: '),
                'password': getpass.getpass()}

    def __init__(self, cred=None, max_tries=5, callback=newcred):
        """Create a new CosignPasswordMgr.

        Args:

          cred: Initial credentials. Will be returned by the first
          call to get_cred(). Should be a dictionary of the form:
            {'login': username, 'password': password}

          max_tries: Maximum number of times get_cred() may be called
          before IndexError is raised.

          callback: A function to be called to get new
          credentials. The current object instance (self) will be
          passed as the first argument.
        """
        self.set_cred(cred)
        self.try_count = 1
        self.max_tries = max_tries
        self.callback = callback

    def set_cred(self, cred):
        """Set stored credentials to cred.

        cred should be of the form:
          {'login': username, 'password': password}
        """
        self.cred = cred
        self.dirty = False

    def get_cred(self):
        """Get new credentials.

        Return a credentials dictionary (see set_cred()). Raise an
        IndexError exception if self.max_tries have already been made.
        """
        if not self.dirty and self.cred is not None:
            self.try_count = self.try_count + 1
            self.dirty = True
            return self.cred

        if self.try_count > self.max_tries:
            raise IndexError("Exceeded max_tries ({})".format(self.max_tries))

        self.cred = self.callback(self)
        self.try_count = self.try_count + 1

        self.dirty = True
        return self.cred

class CosignHandler(urllib.request.BaseHandler):
    """urllib.request style handler for Cosign protected URLs.

    See http://weblogin.org

    SYNOPSIS:

    # Cosign relies on cookies.
    cj = http.cookiejar.MozillaCookieJar('cookies.txt')

    # We need an opener that handles cookies and any cosign redirects and
    # logins.
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj),
        # Here's the CosignHandler.
        CosignHandler('https://cosign.login/page',
                      cj,
                      CosignPasswordMgr()
                      # If you've got one big program you'll probably
                      # want to keep the cookies in memory, but for
                      # lots of little programs we get single sign on
                      # behaviour by saving and loading to/from a
                      # file.
                      save_cookies=True
                      )
        )

    # Construct a request for the page we actually want
    req = urllib.request.Request(
        url='https://some.cosign.protected/url',
        )

    # make the request
    res = opener.open(req)
    # If all went well, res encapsulates the desired result, use res.read()
    # to get at the data and so on.
    """

    def __init__(self, login_url, cj, pw_mgr, save_cookies=True):
        """Construct new CosignHandler.

        Args:
          login_url: URL of cosign login page. Used to figure out if we
            have been redirected to the login page after a failed
            authentication, and as the URL to POST to to log in.

          cj: An http.cookiejar.CookieJar or equivalent. You'll need
            something that implements the FileCookieJar interface if
            you want to load/save cookies.

          pw_mgr: A CosignPasswordMgr object or equivalent. This
            object will provide (and if necessary prompt for) the
            username and password.

          save_cookies: Whether or not to save cookies to a file after
            each request. Required for single sign on between
            different scripts.
        """
        super().__init__()
        self.login_url = login_url
        self.cj = cj
        self.pw_mgr = pw_mgr
        self.save_cookies = save_cookies
        # try to load cookies from file (specified when constructing cj)
        try:
            self.cj.load(ignore_discard=True)
        except IOError:
            pass

    def https_response(self, req, res):
        """Handle https_response.

        If the response is from the cosign login page (starts with
        self.login_url) then log in to cosign and retry. Otherwise
        continue as normal.
        """
        if res.code == 200 and res.geturl().startswith(self.login_url + '?'):
            # Been redirected to login page.

            # We'll need the cosign cookies later
            self.cj.extract_cookies(res, req)

            # Grab a username and password.
            data = urllib.parse.urlencode(self.pw_mgr.get_cred())

            # Construct a login POST request to the login page.
            req2 = urllib.request.Request(
                self.login_url,
                data.encode('iso-8859-1'),
                )
            # We need a different opener that doesn't have a CosignHandler.
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.cj)
                )
            # Try the login
            res2 = opener.open(req2)
            # Cookies, cookies, cookies
            self.cj.extract_cookies(res2, req2)

            # We should be logged in, go back and get what was asked for
            res = opener.open(req)

            # If we end up back at the login page then login failed
            if res.geturl().startswith(self.login_url + '?'):
                raise Exception('Login failed.')

            if self.save_cookies:
                self.cj.extract_cookies(res,req)
                self.cj.save(ignore_discard=True)

        return res
