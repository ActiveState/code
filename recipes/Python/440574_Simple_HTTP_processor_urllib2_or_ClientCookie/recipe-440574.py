import sys
import ClientCookie

class HTTPMyDebugProcessor(ClientCookie.BaseHandler):
    """ Track HTTP requests and responses with this custom handler.
    Be sure to add it last in your build_opener call, or use:
        handler_order = 900 """
    def __init__(self, httpout=sys.stdout):
        self.httpout = httpout

    def http_request(self, request):
        if __debug__:
            host, full_url = request.get_host(), request.get_full_url()
            url_path = full_url[full_url.find(host) + len(host):]
            self.httpout.write("%s\n" % request.get_full_url())
            self.httpout.write('\n')
            self.httpout.write("%s %s\n" % (request.get_method(), url_path))

            for header in request.header_items():
                self.httpout.write("%s: %s\n" % header[:])

            self.httpout.write('\n')

        return request

    def http_response(self, request, response):
        if __debug__:
            code, msg, hdrs = response.code, response.msg, response.info()
            self.httpout.write("HTTP/1.x %s %s\n" % (code, msg))
            self.httpout.write(str(hdrs))

        return response

    https_request = http_request
    https_response = http_response

# Example
cjar = ClientCookie.LWPCookieJar()
opener = ClientCookie.build_opener(
    ClientCookie.HTTPCookieProcessor(cjar),
    ClientCookie.HTTPRefererProcessor(),
    HTTPMyDebugProcessor(),
)
ClientCookie.install_opener(opener)
response = ClientCookie.urlopen("http://www.google.com")
#...
