import os

always_works = 0

def starturl(url, dwell=0, add_msg="", tempfile = "name_ending_in.html"):
    html  = "<html><head>\r\n<meta http-equiv=refresh "
    html += 'content="%s; url=%s">' % (dwell, url)
    html += "\r\n</head><body bgcolor=#d0d0d0>\r\n"
    html += "<h2>Loading .... &nbsp; &nbsp;"
    html += "<a href=%s>%s</a>" % (url,url)
    html += "<p><h3>%s</h3>\r\n</body></html>" % add_msg
    emfile_open_flags = os.O_WRONLY+os.O_CREAT+os.O_TRUNC+os.O_BINARY
    emf = os.open(tempfile, emfile_open_flags)
    os.write(emf, html)
    os.close(emf)
    os.startfile(tempfile)

if __name__ == '__main__':
    if always_works == 1:
        starturl("http://www.python.org")
    else:
        os.startfile("http://www.python.org")
