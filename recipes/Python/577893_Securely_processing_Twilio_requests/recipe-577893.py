# A decorator that lets you require HTTP basic authentication from visitors.
# Kevin Kelley <kelleyk@kelleyk.net> 2011
# Use however makes you happy, but if it breaks, you get to keep both pieces.

# Post with explanation, commentary, etc.:
# http://kelleyk.com/post/7362319243/easy-basic-http-authentication-with-tornado

import base64, logging
import tornado.web
import twilio # From https://github.com/twilio/twilio-python

def require_basic_auth(handler_class):
    def wrap_execute(handler_execute):
        def require_basic_auth(handler, kwargs):
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                handler._transforms = []
                handler.finish()
                return False
            auth_decoded = base64.decodestring(auth_header[6:])
            kwargs['basicauth_user'], kwargs['basicauth_pass'] = auth_decoded.split(':', 2)
            return True
        def _execute(self, transforms, *args, **kwargs):
            if not require_basic_auth(self, kwargs):
                return False
            return handler_execute(self, transforms, *args, **kwargs)
        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class


twilio_account_sid = 'INSERT YOUR ACCOUNT ID HERE'
twilio_account_token = 'INSERT YOUR ACCOUNT TOKEN HERE'

@require_basic_auth
class TwilioRequestHandler(tornado.web.RequestHandler):
    def post(self, basicauth_user, basicauth_pass):
        """
        Receive a Twilio request, return a TwiML response
        """
        # We check in two ways that it's really Twilio POSTing to this URL:
        # 1. Check that Twilio is sending the username and password we specified
        #    for it at https://www.twilio.com/user/account/phone-numbers/incoming
        # 2. Check that Twilio has signed its request with our secret account token
        username = 'CONFIGURE USERNAME AT TWILIO.COM AND ENTER IT HERE'
        password = 'CONFIGURE PASSWORD AT TWILIO.COM AND ENTER IT HERE'
        if basicauth_user != username or basicauth_pass != password:
            raise tornado.web.HTTPError(401, "Invalid username and password for HTTP basic authentication")

        # Construct the URL to this handler.
        # self.request.full_url() doesn't work, because Twilio sort of has a bug:
        # We tell it to POST to our URL with HTTP Authentication like this:
        #   http://username:password@b-date.me/api/twilio_request_handler
        # ... and Twilio uses *that* URL, with username and password included, as
        # part of its signature.
        # Also, if we're proxied by Nginx, then Nginx handles the HTTPS protocol and
        # connects to Tornado over HTTP
        protocol = 'https' if self.request.headers.get('X-Twilio-Ssl') == 'Enabled' else self.request.protocol
        url = '%s://%s:%s@%s%s' % (
            protocol, username, password, self.request.host, self.request.path,
        )

        if not twilio.Utils(twilio_account_sid, twilio_account_token).validateRequest(
            url,
            # arguments has lists like { 'key': [ 'value', ... ] }, so flatten them
            {
                k: self.request.arguments[k][0]
                for k in self.request.arguments
            },
            self.request.headers.get('X-Twilio-Signature'),
        ):
            logging.error("Invalid Twilio signature to %s: %s" % (
                self.request.full_url(), self.request
            ))
            raise tornado.web.HTTPError(401, "Invalid Twilio signature")

        # Do your actual processing of Twilio's POST here, using self.get_argument()
        
