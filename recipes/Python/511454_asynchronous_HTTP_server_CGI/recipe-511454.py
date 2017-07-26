import SimpleAsyncServer

# =============================================================
# An implementation of the HTTP protocol, supporting persistent
# connections and CGI
# =============================================================
import sys
import os
import traceback
import datetime
import mimetypes
import urlparse
import urllib
import cStringIO

class HTTP(SimpleAsyncServer.ClientHandler):
    
    # parameters to override if necessary
    root = os.getcwd()  # the directory to serve files from
    cgi_directories = ['/cgi-bin']  # subdirectories for cgi scripts
    logging = True      # print logging info for each request ?
    blocksize = 2 << 16 # size of blocks to read from files and send

    def request_complete(self):
        """In the HTTP protocol, a request is complete if the "end of headers"
        sequence ('\r\n\r\n') has been received
        If the request is POST, stores the request body in a StringIO before
        returning True"""
        terminator = self.incoming.find('\r\n\r\n')
        if terminator == -1:
            return False
        lines = self.incoming[:terminator].split('\r\n')
        self.requestline = lines[0]
        try:
            self.method,self.url,self.protocol = lines[0].strip().split()
        except:
            self.method = None # indicates bad request
            return True
        # put request headers in a dictionary
        self.headers = {}
        for line in lines[1:]:
            k,v = line.split(':',1)
            self.headers[k.lower().strip()] = v.strip()
        # persistent connection
        close_conn = self.headers.get("connection","")
        if (self.protocol == "HTTP/1.1" 
            and close_conn.lower() == "keep-alive"):
            self.close_when_done = False
        # parse the url
        scheme,netloc,path,params,query,fragment = urlparse.urlparse(self.url)
        self.path,self.rest = path,(params,query,fragment)

        if self.method == 'POST':
            # for POST requests, read the request body
            # its length must be specified in the content-length header
            content_length = int(self.headers.get('content-length',0))
            body = self.incoming[terminator+4:]
            # request is incomplete if not all message body received
            if len(body)<content_length:
                return False
            f_body = cStringIO.StringIO(body)
            f_body.seek(0)
            sys.stdin = f_body # compatibility with CGI

        return True

    def make_response(self):
        """Build the response : a list of strings or files"""
        if self.method is None: # bad request
            return self.error_resp(400,'Bad request : %s' %self.requestline)
        resp_headers, resp_body, resp_file = '','',None
        if not self.method in ['GET','POST','HEAD']:
            return self.err_resp(501,'Unsupported method (%s)' %self.method)
        else:
            file_name = self.file_name = self.translate_path()
            if not os.path.exists(file_name):
                return self.err_resp(404,'File not found')
            elif self.managed():
                response = self.mngt_method()
            else:
                ext = os.path.splitext(file_name)[1]
                c_type = mimetypes.types_map.get(ext,'text/plain')
                resp_line = "%s 200 Ok\r\n" %self.protocol
                size = os.stat(file_name).st_size
                resp_headers = "Content-Type: %s\r\n" %c_type
                resp_headers += "Content-Length: %s\r\n" %size
                resp_headers += '\r\n'
                if self.method == "HEAD":
                    resp_string = resp_line + resp_headers
                elif size > HTTP.blocksize:
                    resp_string = resp_line + resp_headers
                    resp_file = open(file_name,'rb')
                else:
                    resp_string = resp_line + resp_headers + \
                        open(file_name,'rb').read()
                response = [resp_string]
                if resp_file:
                    response.append(resp_file)
        self.log(200)
        return response

    def translate_path(self):
        """Translate URL path into a path in the file system"""
        return os.path.join(HTTP.root,*self.path.split('/'))

    def managed(self):
        """Test if the request can be processed by a specific method
        If so, set self.mngt_method to the method used
        This implementation tests if the script is in a cgi directory"""
        if self.is_cgi():
            self.mngt_method = self.run_cgi
            return True
        return False

    def is_cgi(self):
        """Test if url in a cgi directory"""
        for path in self.cgi_directories:
            if self.path.startswith(path):
                rest = self.path[len(path):]
                if not rest or rest.startswith('/'):
                    return True
        return False

    def run_cgi(self):
        # set CGI environment variables
        self.make_cgi_env()
        # redirect print statements to a cStringIO
        save_stdout = sys.stdout
        sys.stdout = cStringIO.StringIO()
        # run the script
        try:
            execfile(self.file_name)
        except:
            sys.stdout = cStringIO.StringIO()
            sys.stdout.write("Content-type:text/plain\r\n\r\n")
            traceback.print_exc(file=sys.stdout)
        response = sys.stdout.getvalue()
        if self.method == "HEAD":
            # for HEAD request, don't send message body even if the script
            # returns one (RFC 3875)
            head_lines = []
            for line in response.split('\n'):
                if not line:
                    break
                head_lines.append(line)
            response = '\n'.join(head_lines)
        sys.stdout = save_stdout # restore sys.stdout
        # close connection in case there is no content-length header
        self.close_when_done = True
        resp_line = "%s 200 Ok\r\n" %self.protocol
        return [resp_line + response]

    def make_cgi_env(self):
        """Set CGI environment variables"""
        env = {}
        env['SERVER_SOFTWARE'] = "AsyncServer"
        env['SERVER_NAME'] = "AsyncServer"
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['DOCUMENT_ROOT'] = HTTP.root
        env['SERVER_PROTOCOL'] = "HTTP/1.1"
        env['SERVER_PORT'] = str(self.server.port)

        env['REQUEST_METHOD'] = self.method
        env['REQUEST_URI'] = self.url
        env['PATH_TRANSLATED'] = self.translate_path()
        env['SCRIPT_NAME'] = self.path
        env['PATH_INFO'] = urlparse.urlunparse(("","","",self.rest[0],"",""))
        env['QUERY_STRING'] = self.rest[1]
        if not self.host == self.client_address[0]:
            env['REMOTE_HOST'] = self.host
        env['REMOTE_ADDR'] = self.client_address[0]
        env['CONTENT_LENGTH'] = str(self.headers.get('content-length',''))
        for k in ['USER_AGENT','COOKIE','ACCEPT','ACCEPT_CHARSET',
            'ACCEPT_ENCODING','ACCEPT_LANGUAGE','CONNECTION']:
            hdr = k.lower().replace("_","-")
            env['HTTP_%s' %k.upper()] = str(self.headers.get(hdr,''))
        os.environ.update(env)

    def err_resp(self,code,msg):
        """Return an error message"""
        resp_line = "%s %s %s\r\n" %(self.protocol,code,msg)
        self.close_when_done = True
        self.log(code)
        return [resp_line]

    def log(self,code):
        """Write a trace of the request on stderr"""
        if HTTP.logging:
            date_str = datetime.datetime.now().strftime('[%d/%b/%Y %H:%M:%S]')
            sys.stderr.write('%s - - %s "%s" %s\n' %(self.host,
                date_str,self.requestline,code))

if __name__=="__main__":
    # launch the server on the specified port
    port = 8081
    print "Asynchronous HTTP server running on port %s" %port
    print "Press Ctrl+C to stop"
    server = SimpleAsyncServer.Server('', port)
    HTTP.logging = False
    try:
        SimpleAsyncServer.loop(server,HTTP)
    except KeyboardInterrupt:
        for s in server.client_handlers:
            server.close_client(s)
        print 'Ctrl+C pressed. Closing'
