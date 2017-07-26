from httplib import HTTPConnection, _CS_IDLE
import urlparse

def pipeline(domain,pages,max_out_bound=4,debuglevel=0):
    pagecount = len(pages)
    conn = HTTPConnection(domain)
    conn.set_debuglevel(debuglevel)
    respobjs = [None]*pagecount
    finished = [False]*pagecount
    data = [None]*pagecount
    headers = {'Host':domain,'Content-Length':0,'Connection':'Keep-Alive'}

    while not all(finished):
        # Send 
        out_bound = 0
        for i,page in enumerate(pages):
            if out_bound >= max_out_bound:
                break
            elif page and not finished[i] and respobjs[i] is None:
                if debuglevel > 0:
                    print 'Sending request for %r...' % (page,)
                conn._HTTPConnection__state = _CS_IDLE # FU private variable!
                conn.request("GET", page, None, headers)
                respobjs[i] = conn.response_class(conn.sock, strict=conn.strict, method=conn._method)
                out_bound += 1
        # Try to read a response
        for i,resp in enumerate(respobjs):
            if resp is None:
                continue
            if debuglevel > 0:
                print 'Retrieving %r...' % (pages[i],)
            out_bound -= 1
            skip_read = False
            resp.begin()
            if debuglevel > 0:
                print '    %d %s' % (resp.status, resp.reason)
            if 200 <= resp.status < 300:
                # Ok
                data[i] = resp.read()
                cookie = resp.getheader('Set-Cookie')
                if cookie is not None:
                    headers['Cookie'] = cookie
                skip_read = True
                finished[i] = True
                respobjs[i] = None
            elif 300 <= resp.status < 400:
                # Redirect
                loc = resp.getheader('Location')
                respobjs[i] = None
                parsed = loc and urlparse.urlparse(loc)
                if not parsed:
                    # Missing or empty location header
                    data[i] = (resp.status, resp.reason)
                    finished[i] = True
                elif parsed.netloc != '' and parsed.netloc != host:
                    # Redirect to another host
                    data[i] = (resp.status, resp.reason, loc)
                    finished[i] = True
                else:
                    path = urlparse.urlunparse(parsed._replace(scheme='',netloc='',fragment=''))
                    if debuglevel > 0:
                        print '  Updated %r to %r' % (pages[i],path)
                    pages[i] = path
            elif resp.status >= 400:
                # Failed
                data[i] = (resp.status, resp.reason)
                finished[i] = True
                respobjs[i] = None
            if resp.will_close:
                # Connection (will be) closed, need to resend
                conn.close()
                if debuglevel > 0:
                    print '  Connection closed'
                for j,f in enumerate(finished):
                    if not f and respobj[j] is not None:
                        if debuglevel > 0:
                            print '  Discarding out-bound request for %r' % (pages[j],)
                        respobj[j] = None
                break
            elif not skip_read:
                resp.read() # read any data
            if any(not f and respobjs[j] is None for j,f in enumerate(finished)):
                # Send another pending request
                break
        else:
            break # All respobjs are None?
    return data

if __name__ == '__main__':
    domain = 'en.wikipedia.org'
    pages = ('/wiki/HTTP_pipelining', '/wiki/HTTP', '/wiki/HTTP_persistent_connection')
    data = pipeline(domain,pages,max_out_bound=2,debuglevel=1)
    for i,page in enumerate(data):
        print
        print '==== Page %r ====' % (pages[i],)
        print page[:512]
