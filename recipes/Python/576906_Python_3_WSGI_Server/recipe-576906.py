import calendar
import datetime
import email.utils
import hashlib
import http
import logging
import mimetypes
import os.path
import re
import stat
import sys
import time
import urllib


class Application(object):
    """A collection of request handlers that make up a web application."""
    def __init__(self, handlers=None, default_host="", transforms=None,
                 **settings):
        if transforms is None:
            self.transforms = [ChunkedTransferEncoding]
        else:
            self.transforms = transforms
        self.handlers = []
        self.default_host = default_host
        self.settings = settings
        self._wsgi = False
        if self.settings.get('static_path'):
            path = self.settings['static_path']
            handlers = list(handlers or [])
            handlers.extend([
                (r'/static/(.*)', StaticFileHandler, dict(path=path)),
                (r'/(favicon\.ico)', StaticFileHandler, dict(path=path)),
                (r'/(robots\.txt)', StaticFileHandler, dict(path=path)),
            ])
        if handlers: self.add_handlers(".*$", handlers)

    def add_handlers(self, host_pattern, host_handlers):
        """Appends the given handlers to our handler list."""
        if not host_pattern.endswith("$"):
            host_pattern += "$"
        handlers = []
        self.handlers.append((re.compile(host_pattern), handlers))

        for handler_tuple in host_handlers:
            assert len(handler_tuple) in (2, 3)
            pattern = handler_tuple[0]
            handler = handler_tuple[1]
            if len(handler_tuple) == 3:
                kwargs = handler_tuple[2]
            else:
                kwargs = {}
            if not pattern.endswith("$"):
                pattern += "$"
            handlers.append((re.compile(pattern), handler, kwargs))

    def add_transform(self, transform_class):
        """Adds the given OutputTransform to our transform list."""
        self.transforms.append(transform_class)

    def _get_host_handlers(self, request):
        host = request.host.lower().split(':')[0]
        for pattern, handlers in self.handlers:
            if pattern.match(host):
                return handlers
        # Look for default host if not behind load balancer (for debugging)
        if "X-Real-Ip" not in request.headers:
            for pattern, handlers in self.handlers:
                if pattern.match(self.default_host):
                    return handlers
        return None

    def __call__(self, request):
        """Called by HTTPServer to execute the request."""
        transforms = [t(request) for t in self.transforms]
        handler = None
        args = []
        handlers = self._get_host_handlers(request)
        if not handlers: 
            handler = RedirectHandler(
                request, "http://" + self.default_host + "/")
        else:
            for pattern, handler_class, kwargs in handlers:
                match = pattern.match(request.path)
                if match:
                    handler = handler_class(self, request, **kwargs)
                    args = match.groups()
                    break
            if not handler:
                handler = ErrorHandler(self, request, 404)

        # In debug mode, re-compile templates and reload static files on every
        # request so you don't need to restart to see changes
        if self.settings.get("debug"):
            RequestHandler._templates = None
            RequestHandler._static_hashes = {}

        handler._execute(transforms, *args)
        return handler


class OutputTransform(object):
    """A transform modifies the result of an HTTP request (e.g., GZip encoding)

    A new transform instance is created for every request. The sequence of
    calls is:

         t = Transform(request) # Constructor
         # Request processing
         headers = t.transform_headers(headers)
         # Write headers
         for block in result:
             write(t.transform_chunk(block)
         write(t.footer())

    See the ChunkedTransferEncoding example below if you want to implement a
    new Transform.
    """
    def __init__(self, request):
        pass

    def transform_headers(self, headers):
        return headers

    def transform_chunk(self, block):
        return block

    def footer(self):
        return None


class ChunkedTransferEncoding(OutputTransform):
    """Applies the chunked transfer encoding to the response.

    See http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.6.1
    """
    def __init__(self, request):
        self._chunking = request.supports_http_1_1()

    def transform_headers(self, headers):
        if self._chunking:
            # No need to chunk the output if a Content-Length is specified
            if "Content-Length" in headers or "Transfer-Encoding" in headers:
                self._chunking = False
            else:
                headers["Transfer-Encoding"] = "chunked"
        return headers

    def transform_chunk(self, block):
        if self._chunking:
            return ("%x" % len(block)) + "\r\n" + block + "\r\n"
        else:
            return block

    def footer(self):
        if self._chunking:
            return "0\r\n\r\n"
        else:
            return None


class RequestHandler(object):
    """Subclass this class and define get() or post() to make a handler.

    If you want to support more methods than the standard GET/HEAD/POST, you
    should override the class variable SUPPORTED_METHODS in your
    RequestHandler class.
    """
    SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PUT")

    def __init__(self, application, request, transforms=None):
        self.application = application
        self.request = request
        self._headers_written = False
        self._finished = False
        self._auto_finish = True
        self._transforms = transforms or []
        self.clear()

    @property
    def settings(self):
        return self.application.settings

    def head(self, *args, **kwargs):
        raise HTTPError(405)

    def get(self, *args, **kwargs):
        raise HTTPError(405)

    def post(self, *args, **kwargs):
        raise HTTPError(405)

    def delete(self, *args, **kwargs):
        raise HTTPError(405)

    def put(self, *args, **kwargs):
        raise HTTPError(405)

    def prepare(self):
        """Called before the actual handler method.

        Useful to override in a handler if you want a common bottleneck for
        all of your requests.
        """
        pass

    def clear(self):
        """Resets all headers and content for this response."""
        self._headers = {
            "Server": "TornadoServer/0.1",
            "Content-Type": "text/html; charset=UTF-8",
        }
        if not self.request.supports_http_1_1():
            if self.request.headers.get("Connection") == "Keep-Alive":
                self.set_header("Connection", "Keep-Alive")
        self._write_buffer = []
        self._status_code = 200

    def set_status(self, status_code):
        """Sets the status code for our response."""
        assert status_code in http.client.responses
        self._status_code = status_code

    def set_header(self, name, value):
        """Sets the given response header name and value.

        If a datetime is given, we automatically format it according to the
        HTTP specification. If the value is not a string, we convert it to
        a string. All header values are then encoded as UTF-8.
        """
        if isinstance(value, datetime.datetime):
            t = calendar.timegm(value.utctimetuple())
            value = email.utils.formatdate(t, localtime=False, usegmt=True)
        elif isinstance(value, int):
            value = str(value)
        else:
            value = str(value)
            # If \n is allowed into the header, it is possible to inject
            # additional headers or split the request. Also cap length to
            # prevent obviously erroneous values.
            safe_value = re.sub(r"[\x00-\x1f]", " ", value)[:4000]
            if safe_value != value:
                raise ValueError("Unsafe header value %r", value)
        self._headers[name] = value

    _ARG_DEFAULT = []
    def get_argument(self, name, default=_ARG_DEFAULT, strip=True):
        """Returns the value of the argument with the given name.

        If default is not provided, the argument is considered to be
        required, and we throw an HTTP 404 exception if it is missing.

        The returned value is always unicode.
        """
        values = self.request.arguments.get(name, None)
        if values is None:
            if default is self._ARG_DEFAULT:
                raise HTTPError(404, "Missing argument %s" % name)
            return default
        # Get rid of any weird control chars
        value = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", values[-1])
        value = _unicode(value)
        if strip: value = value.strip()
        return value

    def redirect(self, url, permanent=False):
        """Sends a redirect to the given (optionally relative) URL."""
        if self._headers_written:
            raise Exception("Cannot redirect after headers have been written")
        self.set_status(301 if permanent else 302)
        # Remove whitespace
        url = re.sub(r"[\x00-\x20]+", "", str(url))
        self.set_header("Location", urlparse.urljoin(self.request.uri, url))
        self.finish()

    def write(self, chunk):
        """Writes the given chunk to the output buffer.

        To write the output to the network, use the flush() method below.

        If the given chunk is a dictionary, we write it as JSON and set
        the Content-Type of the response to be text/javascript.
        """
        assert not self._finished
        if isinstance(chunk, dict):
            chunk = escape.json_encode(chunk)
            self.set_header("Content-Type", "text/javascript; charset=UTF-8")
        chunk = str(chunk)
        self._write_buffer.append(chunk)

    def flush(self, include_footers=False):
        """Flushes the current output buffer to the nextwork."""
        if self.application._wsgi:
            raise Exception("WSGI applications do not support flush()")
        if not self._headers_written:
            self._headers_written = True
            headers = self._generate_headers()
        else:
            headers = ""

        # Ignore the chunk and only write the headers for HEAD requests
        if self.request.method == "HEAD":
            if headers: self.request.write(headers)
            return

        if self._write_buffer:
            chunk = "".join(self._write_buffer)
            self._write_buffer = []
            if chunk:
                # Don't write out empty chunks because that means
                # END-OF-STREAM with chunked encoding
                for transform in self._transforms:
                    chunk = transform.transform_chunk(chunk)
        else:
            chunk = ""
        if include_footers:
            footers = []
            for transform in self._transforms:
                footer = transform.footer()
                if footer: chunk += footer

        if headers or chunk:
            self.request.write(headers + chunk)

    def finish(self, chunk=None):
        """Finishes this response, ending the HTTP request."""
        assert not self._finished
        if chunk: self.write(chunk)

        # Automatically support ETags and add the Content-Length header if
        # we have not flushed any content yet.
        if not self._headers_written:
            if self._status_code == 200 and self.request.method == "GET":
                hasher = hashlib.sha1()
                for part in self._write_buffer:
                    hasher.update(part.encode('ascii'))
                etag = '"%s"' % hasher.hexdigest()
                inm = self.request.headers.get("If-None-Match")
                if inm and inm.find(etag) != -1:
                    self._write_buffer = []
                    self.set_status(304)
                else:
                    self.set_header("Etag", etag)
            if "Content-Length" not in self._headers:
                content_length = sum(len(part) for part in self._write_buffer)
                self.set_header("Content-Length", content_length)

        if not self.application._wsgi:
            self.flush(include_footers=True)
            self.request.finish()
            self._log()
        self._finished = True

    def send_error(self, status_code=500):
        """Sends the given HTTP error code to the browser.

        We also send the error HTML for the given error code as returned by
        get_error_html. Override that method if you want custom error pages
        for your application.
        """
        if self._headers_written:
            logging.error("Cannot send error response after headers written")
            if not self._finished:
                self.finish()
            return
        self.clear()
        self.set_status(status_code)
        message = self.get_error_html(status_code)
        self.finish(message)

    def get_error_html(self, status_code):
        """Override to implement custom error pages."""
        return "<html><title>%(code)d: %(message)s</title>" \
               "<body>%(code)d: %(message)s</body></html>" % {
            "code": status_code,
            "message": http.client.responses[status_code],
        }

    @property
    def locale(self):
        """The local for the current session.

        Determined by either get_user_locale, which you can override to
        set the locale based on, e.g., a user preference stored in a
        database, or get_browser_locale, which uses the Accept-Language
        header.
        """
        if not hasattr(self, "_locale"):
            self._locale = self.get_browser_locale()
            assert self._locale
        return self._locale

    def get_browser_locale(self, default="en_US"):
        """Determines the user's locale from Accept-Language header.

        See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.4
        """
        if "Accept-Language" in self.request.headers:
            languages = self.request.headers["Accept-Language"].split(",")
            locales = []
            for language in languages:
                parts = language.strip().split(";")
                if len(parts) > 1 and parts[1].startswith("q="):
                    try:
                        score = float(parts[1][2:])
                    except (ValueError, TypeError):
                        score = 0.0
                else:
                    score = 1.0
                locales.append((parts[0], score))
            if locales:
                locales.sort(key=lambda l: l[1], reverse=True)
                codes = [l[0] for l in locales]
                return locale.get(*codes)
        return locale.get(default)

    def static_url(self, path):
        """Returns a static URL for the given relative static file path.

        This method requires you set the 'static_path' setting in your
        application (which specifies the root directory of your static
        files).

        We append ?v=<signature> to the returned URL, which makes our
        static file handler set an infinite expiration header on the
        returned content. The signature is based on the content of the
        file.

        If this handler has a "include_host" attribute, we include the
        full host for every static URL, including the "http://". Set
        this attribute for handlers whose output needs non-relative static
        path names.
        """
        self.require_setting("static_path", "static_url")
        if not hasattr(RequestHandler, "_static_hashes"):
            RequestHandler._static_hashes = {}
        hashes = RequestHandler._static_hashes
        if path not in hashes:
            try:
                f = open(os.path.join(
                    self.application.settings["static_path"], path))
                hashes[path] = hashlib.md5(f.read()).hexdigest()
                f.close()
            except:
                logging.error("Could not open static file %r", path)
                hashes[path] = None
        base = self.request.protocol + "://" + self.request.host \
            if getattr(self, "include_host", False) else ""
        if hashes.get(path):
            return base + "/static/" + path + "?v=" + hashes[path][:5]
        else:
            return base + "/static/" + path

    def async_callback(self, callback, *args, **kwargs):
        """Wrap callbacks with this if they are used on asynchronous requests.

        Catches exceptions and properly finishes the request.
        """
        if callback is None:
            return None
        if args or kwargs:
            callback = functools.partial(callback, *args, **kwargs)
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except Exception as e:
                if self._headers_written:
                    logging.error("Exception after headers written",
                                  exc_info=True)
                else:
                    self._handle_request_exception(e)
        return wrapper

    def require_setting(self, name, feature="this feature"):
        """Raises an exception if the given app setting is not defined."""
        if not self.application.settings.get(name):
            raise Exception("You must define the '%s' setting in your "
                            "application to use %s" % (name, feature))

    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            self.prepare()
            if not self._finished:  
                getattr(self, self.request.method.lower())(*args, **kwargs)
                if self._auto_finish and not self._finished:
                    self.finish()
        except Exception as e:
            self._handle_request_exception(e)

    def _generate_headers(self):
        for transform in self._transforms:
            headers = transform.transform_headers(self._headers)
        lines = [self.request.version + " " + str(self._status_code) + " " +
                 http.client.responses[self._status_code]]
        lines.extend(["%s: %s" % (n, v) for n, v in self._headers.iteritems()])
        return "\r\n".join(lines) + "\r\n\r\n"

    def _log(self):
        if self._status_code < 400:
            log_method = logging.info
        elif self._status_code < 500:
            log_method = logging.warning
        else:
            log_method = logging.error
        request_time = 1000.0 * self.request.request_time()
        log_method("%d %s %.2fms", self._status_code,
                   self._request_summary(), request_time)

    def _request_summary(self):
        return self.request.method + " " + self.request.uri + " (" + \
            self.request.remote_ip + ")"

    def _handle_request_exception(self, e):
        if isinstance(e, HTTPError):
            if e.log_message:
                format = "%d %s: " + e.log_message
                args = [e.status_code, self._request_summary()] + list(e.args)
                logging.warning(format, *args)
            if e.status_code not in http.client.responses:
                logging.error("Bad HTTP status code: %d", e.status_code)
                self.send_error(500)
            else:
                self.send_error(e.status_code)
        else:
            logging.error("Uncaught exception %s\n%r", self._request_summary(),
                          self.request, exc_info=e)
            self.send_error(500)


class HTTPRequest(object):
    """Mimics httpserver.HTTPRequest for WSGI applications."""
    def __init__(self, environ):
        """Parses the given WSGI environ to construct the request."""
        self.method = environ["REQUEST_METHOD"]
        self.path = urllib.parse.quote(environ.get("SCRIPT_NAME", ""))
        self.path += urllib.parse.quote(environ.get("PATH_INFO", ""))
        self.uri = self.path
        self.arguments = {}
        self.query = environ.get("QUERY_STRING", "")
        if self.query:
            self.uri += "?" + self.query
            arguments = cgi.parse_qs(self.query)
            for name, values in arguments.iteritems():
                values = [v for v in values if v]
                if values: self.arguments[name] = values
        self.version = "HTTP/1.1"
        self.headers = HTTPHeaders()
        if environ.get("CONTENT_TYPE"):
            self.headers["Content-Type"] = environ["CONTENT_TYPE"]
        if environ.get("CONTENT_LENGTH"):
            self.headers["Content-Length"] = int(environ["CONTENT_LENGTH"])
        for key in environ:
            if key.startswith("HTTP_"):
                self.headers[key[5:].replace("_", "-")] = environ[key]
        if self.headers.get("Content-Length"):
            self.body = environ["wsgi.input"].read()
        else:
            self.body = ""
        self.protocol = environ["wsgi.url_scheme"]
        self.remote_ip = environ.get("REMOTE_ADDR", "")
        if environ.get("HTTP_HOST"):
            self.host = environ["HTTP_HOST"]
        else:
            self.host = environ["SERVER_NAME"]

        # Parse request body
        self.files = {}
        content_type = self.headers.get("Content-Type", "")
        if content_type.startswith("application/x-www-form-urlencoded"):
            for name, values in cgi.parse_qs(self.body).iteritems():
                self.arguments.setdefault(name, []).extend(values)
        elif content_type.startswith("multipart/form-data"):
            boundary = content_type[30:]
            if boundary: self._parse_mime_body(boundary)

        self._start_time = time.time()
        self._finish_time = None

    def supports_http_1_1(self):
        """Returns True if this request supports HTTP/1.1 semantics"""
        return self.version == "HTTP/1.1"

    def full_url(self):
        """Reconstructs the full URL for this request."""
        return self.protocol + "://" + self.host + self.uri

    def request_time(self):
        """Returns the amount of time it took for this request to execute."""
        if self._finish_time is None:
            return time.time() - self._start_time
        else:
            return self._finish_time - self._start_time

    def _parse_mime_body(self, boundary):
        if self.body.endswith("\r\n"):
            footer_length = len(boundary) + 6
        else:
            footer_length = len(boundary) + 4
        parts = self.body[:-footer_length].split("--" + boundary + "\r\n")
        for part in parts:
            if not part: continue
            eoh = part.find("\r\n\r\n")
            if eoh == -1:
                logging.warning("multipart/form-data missing headers")
                continue
            headers = HTTPHeaders.parse(part[:eoh])
            name_header = headers.get("Content-Disposition", "")
            if not name_header.startswith("form-data;") or \
               not part.endswith("\r\n"):
                logging.warning("Invalid multipart/form-data")
                continue
            value = part[eoh + 4:-2]
            name_values = {}
            for name_part in name_header[10:].split(";"):
                name, name_value = name_part.strip().split("=", 1)
                name_values[name] = name_value.strip('"').decode("utf-8")
            if not name_values.get("name"):
                logging.warning("multipart/form-data value missing name")
                continue
            name = name_values["name"]
            if name_values.get("filename"):
                ctype = headers.get("Content-Type", "application/unknown")
                self.files.setdefault(name, []).append(dict(
                    filename=name_values["filename"], body=value,
                    content_type=ctype))
            else:
                self.arguments.setdefault(name, []).append(value)


class HTTPError(Exception):
    """An exception that will turn into an HTTP error response."""
    def __init__(self, status_code, log_message=None, *args):
        self.status_code = status_code
        self.log_message = log_message
        self.args = args

    def __str__(self):
        message = "HTTP %d: %s" % (
            self.status_code, http.client.responses[self.status_code])
        if self.log_message:
            return message + " (" + (self.log_message % self.args) + ")"
        else:
            return message


class ErrorHandler(RequestHandler):
    """Generates an error response with status_code for all requests."""
    def __init__(self, application, request, status_code):
        RequestHandler.__init__(self, application, request)
        self.set_status(status_code)

    def prepare(self):
        raise HTTPError(self._status_code)


class HTTPHeaders(dict):
    """A dictionary that maintains Http-Header-Case for all keys."""
    def __setitem__(self, name, value):
        dict.__setitem__(self, self._normalize_name(name), value)

    def __getitem__(self, name):
        return dict.__getitem__(self, self._normalize_name(name))

    def _normalize_name(self, name):
        return sys.intern("-".join([w.capitalize() for w in name.split("-")]))


class StaticFileHandler(RequestHandler):
    """A simple handler that can serve static content from a directory.

    To map a path to this handler for a static data directory /var/www,
    you would add a line to your application like:

        application = web.Application([
            (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www"}),
        ])

    The local root directory of the content should be passed as the "path"
    argument to the handler.

    To support aggressive browser caching, if the argument "v" is given
    with the path, we set an infinite HTTP expiration header. So, if you
    want browsers to cache a file indefinitely, send them to, e.g.,
    /static/images/myimage.png?v=xxx.
    """
    def __init__(self, application, request, path):
        RequestHandler.__init__(self, application, request)
        self.root = os.path.abspath(path) + "/"

    def head(self, path):
        self.get(path, include_body=False)

    def get(self, path, include_body=True):
        abspath = os.path.abspath(os.path.join(self.root, path))
        if not abspath.startswith(self.root):
            raise HTTPError(403, "%s is not in root static directory", path)
        if not os.path.exists(abspath):
            raise HTTPError(404)
        if not os.path.isfile(abspath):
            raise HTTPError(403, "%s is not a file", path)

        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        stat_result = os.stat(abspath)
        modified = datetime.datetime.fromtimestamp(stat_result[stat.ST_MTIME])
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            date_tuple = email.utils.parsedate(ims_value)
            if_since = datetime.datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return

        self.set_header("Last-Modified", modified)
        self.set_header("Content-Length", stat_result[stat.ST_SIZE])
        if "v" in self.request.arguments:
            self.set_header("Expires", datetime.datetime.utcnow() + \
                                       datetime.timedelta(days=365*10))
            self.set_header("Cache-Control", "max-age=" + str(86400*365*10))
        else:
            self.set_header("Cache-Control", "public")
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        if not include_body:
            return
        file = open(abspath, "r")
        try:
            self.write(file.read())
        finally:
            file.close()


class WSGIApplication(Application):
    """A WSGI-equivalent of web.Application.

    We support the same interface, but handlers running in a WSGIApplication
    do not support flush() or asynchronous methods.
    
    Example usage:

        import web
        import wsgiref.simple_server

        class MainHandler(web.RequestHandler):
            def get(self):
                self.write("Hello, world")

        if __name__ == "__main__":
            application = web.WSGIApplication([
                (r"/", MainHandler),
            ])
            server = wsgiref.simple_server.make_server('', 8888, application)
            server.serve_forever()
    """
    def __init__(self, handlers=None, default_host="", **settings):
        Application.__init__(self, handlers, default_host, transforms=[],
                                 **settings)
        self._wsgi = True

    def __call__(self, environ, start_response):
        handler = Application.__call__(self, HTTPRequest(environ))
        assert handler._finished
        status = str(handler._status_code) + " " + \
            http.client.responses[handler._status_code]
        headers = handler._headers.items()
        start_response(status, headers)
        return handler._write_buffer
