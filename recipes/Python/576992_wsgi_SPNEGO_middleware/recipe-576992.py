from base64 import b64decode
import kerberos, commands

class KerberosAuth:
    def __init__(self, wrapped, realm, service='HTTP'):
        self.realm=realm
        self.service=service
        self.wrapped=wrapped

    def __call__(self, environ, start_response):
        def error():
            start_response('500 Error', [
                ('content-type', 'text/plain'),
            ])
            return ['Internal error']
        def noauth():
            start_response('401 Unauthorized', [
                ('content-type', 'text/plain'),
                ('WWW-Authenticate','Negotiate'),
                ('WWW-Authenticate','Basic realm="Secured area"')
            ])
            return ['No auth']


        if 'HTTP_AUTHORIZATION' not in environ:
            return noauth()

        type, authstr = environ['HTTP_AUTHORIZATION'].split(' ', 1)

        if type == 'Negotiate':
            result, context = kerberos.authGSSServerInit(self.service)
            if result != 1:
                return error()

            gssstring=''
            r=kerberos.authGSSServerStep(context,authstr)
            if r == 1:
                gssstring=kerberos.authGSSServerResponse(context)
            else:
                return noauth()
            def new_start_response(status, headers):
                start_response(
                    status,
                    [
                        ('WWW-Authenticate','Negotiate %s' % gssstring)
                    ]+headers
                )

            environ['REMOTE_USER']=kerberos.authGSSServerUserName(context)
            kerberos.authGSSServerClean(context)
        elif type == 'Basic':
            username, password = b64decode(authstr).split(':',1)
            try:
                kerberos.checkPassword(username, password, self.service, self.realm)
            except:
                return noauth()
            new_start_response=start_response
            environ['REMOTE_USER']=username
        return self.wrapped(environ, new_start_response)

application=KerberosAuth(myApplication, 'REALM.MY.DOMAIN.COM')
