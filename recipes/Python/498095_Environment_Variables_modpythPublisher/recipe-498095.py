def index(req):
    req.content_type = "text/html"

    req.add_common_vars()
    env_vars = req.subprocess_env.copy()

    req.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
    req.write('<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">')
    req.write('<head><title>mod_python.publisher</title></head>')
    req.write('<body>')
    req.write('<h1>Environment Variables</h1>')
    req.write('<table border="1">')
    for key in env_vars:
        req.write('<tr><td>%s</td><td>%s</td></tr>' % (key, env_vars[key]))
    req.write('</table>')
    req.write('</body>')
    req.write('</html>')
