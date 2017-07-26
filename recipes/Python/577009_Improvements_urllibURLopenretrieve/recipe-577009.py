from urllib import quote_plus, FancyURLopener, URLopener, unwrap,\
                   toBytes, splittype


def retrieve(self, url, filename=None, reporthook=None, data=None,
             maxtries=5, r_range=None):
    """retrieve(url) returns (filename, headers) for a local object
    or (tempfilename, headers) for a remote object.
    If it fails, it relaunches itself until the dl is complete or
    maxtries == 0 (maxtries == -1 for unlimited tries).
    Range tuple(start, end) indicates the range of the remote object
    we have to retrieve (ignored for local files)"""
    
    if maxtries < -1:
        raise ValueError, 'maxtries must be at least equal with -1'
    
    url = unwrap(toBytes(url))
    
    if self.tempcache and url in self.tempcache:
        return self.tempcache[url]
    
    type, url1 = splittype(url)
    
    if filename is None and (not type or type == 'file'):
        try:
            fp = self.open_local_file(url1)
            hdrs = fp.info()
            fp.close()
            
            return url2pathname(splithost(url1)[1]), hdrs
        except IOError, msg:
            pass
    
    if not r_range is None:
        try:
            self.addheader(('Range', 'bytes=%d-%d' % r_range))
        except TypeError:
            raise ValueError, 'r_range argument must be a tuple of two int : (start, end)'
            
    
    fp = self.open(url, data)
    
    try:
        headers = fp.info()
        
        if filename:
            tfp = open(filename, 'ab')
        else:
            import tempfile
            
            garbage, path = splittype(url)
            garbage, path = splithost(path or "")
            
            path, garbage = splitquery(path or "")
            path, garbage = splitattr(path or "")
            
            suffix = os.path.splitext(path)[1]
            
            (fd, filename) = tempfile.mkstemp(suffix)
            
            self.__tempfiles.append(filename)
            
            tfp = os.fdopen(fd, 'ab')
        try:
            result = filename, headers
            
            if self.tempcache is not None:
                self.tempcache[url] = result
            
            bs = 1024*8
            size = -1
            read = 0
            blocknum = 0
            
            if "content-length" in headers:
                size = int(headers["Content-Length"])
            elif r_range is not None:
                size = r_range[1]
            
            if reporthook:
                reporthook(blocknum, bs, size)
            
            while 1:
                block = fp.read(bs)
                
                if block == "":
                    break
                
                read += len(block)
                tfp.write(block)
                blocknum += 1
                
                if reporthook:
                    reporthook(blocknum, bs, size)
        finally:
            tfp.close()
    finally:
        fp.close()
    
    # raise exception if actual size does not match content-length 
    # header and if maxtries <= 0
    if size >= 0 and read < size:
        if maxtries > 0 or maxtries == -1:
            self.retrieve(url, filename, reporthook, data, 
                            maxtries if maxtries == -1 else maxtries-1,
                            r_range=(read, size))
        else:
            raise ContentTooShortError("retrieval incomplete: got only %i out "
                                       "of %i bytes" % (read, size), result)

    return result

#to use our function in the opener
URLopener.retrieve = retrieve
