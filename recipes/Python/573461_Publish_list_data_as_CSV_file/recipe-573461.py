def expose_as_csv(f):
    @expose()
    @strongly_expire
    def wrap(*args, **kw):
        rows = f(*args, **kw)
        out = StringIO.StringIO()
        writer = csv.writer(out) #quoting=csv.QUOTE_ALL
        writer.writerows(rows)
        cherrypy.response.headerMap["Content-Type"] = "text/csv"
        cherrypy.response.headerMap["Content-Length"] = out.len
        return out.getvalue()
    return wrap


# Usage
class Root(...

    @expose_as_csv
    def somereport_csv(self):
        data = [('a', 1), ('b', 2), ('c', 3)]
        return data

# Test
wget http://yourdomain/somereport.csv
