import md5
import time

class DigestAuth:
    def __init__(self, realm, users):
        """Incomplete Python implementation of Digest Authentication.

        For the full specification. http://www.faqs.org/rfcs/rfc2617.html

        realm = AuthName in httpd.conf
        users = a dict of users containing {username:password}
        """
        self.realm = realm
        self.users = users
        self._headers= []
        self.params = {}

    def H(self, data):
        return md5.md5(data).hexdigest()

    def KD(self, secret, data):
        return self.H(secret + ":" + data)

    def A1(self):
        # If the "algorithm" directive's value is "MD5" or is
        # unspecified, then A1 is:
        # A1 = unq(username-value) ":" unq(realm-value) ":" passwd
        username = self.params["username"]
        passwd = self.users.get(username, "")
        return "%s:%s:%s" % (username, self.realm, passwd)
        # This is A1 if qop is set
        # A1 = H( unq(username-value) ":" unq(realm-value) ":" passwd )
        #         ":" unq(nonce-value) ":" unq(cnonce-value)

    def A2(self):
        # If the "qop" directive's value is "auth" or is unspecified, then A2 is:
        # A2 = Method ":" digest-uri-value
        return self.method + ":" + self.uri
        # Not implemented
        # If the "qop" value is "auth-int", then A2 is:
        # A2 = Method ":" digest-uri-value ":" H(entity-body)

    def response(self):
        if self.params.has_key("qop"):
            # Check? and self.params["qop"].lower()=="auth":
            # If the "qop" value is "auth" or "auth-int":
            # request-digest  = <"> < KD ( H(A1),     unq(nonce-value)
            #                              ":" nc-value
            #                              ":" unq(cnonce-value)
            #                              ":" unq(qop-value)
            #                              ":" H(A2)
            #                      ) <">
            return self.KD(self.H(self.A1()), \
                           self.params["nonce"] 
                           + ":" + self.params["nc"]
                           + ":" + self.params["cnonce"]
                           + ":" + self.params["qop"]                    
                           + ":" + self.H(self.A2()))
        else:
            # If the "qop" directive is not present (this construction is
            # for compatibility with RFC 2069):
            # request-digest  =
            #         <"> < KD ( H(A1), unq(nonce-value) ":" H(A2) ) > <">
            return self.KD(self.H(self.A1()), \
                           self.params["nonce"] + ":" + self.H(self.A2()))
    
    def _parseHeader(self, authheader):
        try:
            n = len("Digest ")
            authheader = authheader[n:].strip()
            items = authheader.split(", ")
            keyvalues = [i.split("=", 1) for i in items]
            keyvalues = [(k.strip(), v.strip().replace('"', '')) for k, v in keyvalues]
            self.params = dict(keyvalues)
        except:
            self.params = []

    def _returnTuple(self, code):
        return (code, self._headers, self.params.get("username", ""))

    def _createNonce(self):
        return md5.md5("%d:%s" % (time.time(), self.realm)).hexdigest()

    def createAuthheaer(self):
        self._headers.append((
            "WWW-Authenticate", 
            'Digest realm="%s", nonce="%s", algorithm="MD5", qop="auth"'
            % (self.realm, self._createNonce())
            ))

    def authenticate(self, method, uri, authheader=""):
        """ Check the response for this method and uri with authheader

        returns a tuple with:
          - HTTP_CODE
          - a tuple with header info (key, value) or None
          - and the username which was authenticated or None
        """
        self.method = method
        self.uri = uri
        if authheader.strip() == "":
            self.createAuthheaer()
            return self._returnTuple(401)
        self._parseHeader(authheader)
        if not len(self.params):
            return self._returnTuple(400)
        # Check for required parameters
        required = ["username", "realm", "nonce", "uri", "response"]
        for k in required:
            if not self.params.has_key(k):
                return self._returnTuple(400)
        # If the user is unknown we can deny access right away
        if not self.users.has_key(self.params["username"]):
            self.createAuthheaer()
            return self._returnTuple(401)
        # If qop is sent then cnonce and cn MUST be present
        if self.params.has_key("qop"):
            if not self.params.has_key("cnonce") \
               and self.params.has_key("cn"):
                return self._returnTuple(400)
        # All else is OK, now check the response.
        if self.response() == self.params["response"]:
            return self._returnTuple(200)
        else:
            self.createAuthheaer()
            return self._returnTuple(401)
