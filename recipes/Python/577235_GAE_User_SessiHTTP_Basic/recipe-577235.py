"""
A simple script to handle HTTP Basic authentication for Google App Engine
clients. The trick here is that there is no other session support than the 
GAE internal authorized user handling. Which however does not support HTTP
Basic, an auth protocol which is easy to use (for small, scripted clients).
"""
import os, logging, functools, base64

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.api import users

import gauth


MY_APPSPOT = 'my-app'
logger = logging.getLogger(__name__)

def user(method):
    " Prefix the user to method call args. Must have ACSID cookie to log in.  "
    @functools.wraps(method)
    def user_deco(self, *args):
        user = users.get_current_user()
        assert isinstance(user, users.User), "%r" % user
        return method(self, user, *args)              
    return user_deco

def http_basic_auth(method):
    " Prefix user to method call. Authenticates using HTTP Basic Authorization.  "
    @functools.wraps(method)
    def http_basic_auth_deco(self, *args):
        user = users.get_current_user()
        if not user:
            basic_auth = self.request.headers.get('Authorization')
            if not basic_auth:
                logger.debug("Request does not carry auth.")
                self.fail_basic_auth()
                return
            username, password = '', ''
            try:
                user_info = base64.decodestring(basic_auth[6:])
                username, password = user_info.split(':')
            except:
                raise Exception, "Could not parse HTTP Authorization. "
            cookie = None
            try:
                cookie = gauth.do_auth(MY_APPSPOT, username, password, 
                        dev=self.is_devhost())
            except gauth.AuthError, e:
                logger.info("Got a failed login attempt for Google Accounts %r", 
                        username)
                self.fail_auth()
                return
            self.response.set_status(302, 'Use Cookie')
            # Give ACSID cookie to client
            self.response.headers['Set-Cookie'] = cookie
            # Then redirect so clients logs into user-framework
            # XXX: dont use internal redir b/c it resets self.response
            self.response.headers['Location'] = self.request.path
            return
        elif 'Authorization' in self.request.headers:
            # FIXME: ignore or act on (new?) credentials
            assert 'USER_ID' in os.environ
            # XXX: just delete and ignore
            del self.request.headers['Authorization']
            del os.environ['HTTP_AUTHORIZATION']
            # XXX: this may happen once if a client retries auth on 302
            logger.warning("Ignored HTTP Authorization.")
        assert isinstance(user, users.User), "%r" % user
        return method(self, user, *args)              
    return http_basic_auth_deco


# Abstract handlers

class MyRequestHandler(webapp.RequestHandler):

    def is_devhost(self):
        return not self.request.host.endswith('.appspot.com')

class MyAuthorizedHandler(MyRequestHandler):

    def fail_auth(handler):
        handler.error(401)

    def fail_basic_auth(handler):
        handler.fail_auth()
        handler.response.headers['WWW-Authenticate'] = \
                'Basic realm="Google Accounts for %s.appspot.com."' % MY_APPSPOT

# Request handlers

class MyAuthenticationEndpoint(MyAuthorizedHandler):
    urlp = 'my-auth$'

    @http_basic_auth
    def get(self, user):
        logger.info("User was logged in: %r", user)
        self.response.out.write("%s <a href='%s'>logout</a>" % (
                user.email(),
                users.create_logout_url(self.request.url),))

class MyAuthenticatedEndpoint(MyAuthorizedHandler):
    urlp = 'some-leaf$'

    @user
    def get(self, user):
        logger.info("User %r requested %r", user, self.request.url)
        self.response.out.write("%s <a href='%s'>logout</a>" % (
                user.email(),
                users.create_logout_url(self.request.url),))


application = webapp.WSGIApplication(map(
    lambda h: ('^/'+h.urlp, h), [ # map from URL-path-pattern @ RequestHandler
        MyAuthenticationEndpoint,
        MyAuthenticatedEndpoint,
    ]), debug=True)


def webapp_main():
    """Run within webapp framework.
    """
    # Ofcourse, instead allowing solely Google Accounts and using the integrated
    # system, this recipe could be extended to also login other accounts.
    # However, there the automatic Cookie checking would obviously fail and you
    # would need to do ones own checking. Possibly by using a session instead of
    # cookies, by using other cookies, or by simply having each HTTP request
    # Authorized; unlike this recipe. This is two-legged authentication, so the 
    # latter would not be advised (doing (re)authentication for repeated requests). 
    #from gaesessions import SessionMiddleware
    #run_wsgi_app(SessionMiddleware(application))

    run_wsgi_app(application)

if __name__ == '__main__':
    webapp_main()
