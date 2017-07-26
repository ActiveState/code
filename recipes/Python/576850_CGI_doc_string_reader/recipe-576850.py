import cgi
import cgitb; cgitb.enable()

write = cgi.sys.stdout.write

write('Content-Type: text/html\n\n')

form = cgi.FieldStorage()
module = form.getfirst('m')
write('<head><title> %s </title></head>' % module)
try:
    mod = __import__(module)
except:
    write('<b> Could not import module named %s <br><br> Usage: http://%s%s?m=moduleName</b>' % (module, cgi.os.environ['server_name'],
                                                                                         cgi.os.environ['script_name']))
    cgi.sys.exit()

write('<table border="0" bgcolor="#707070" cellpadding="4" cellspacing="2" width="800" align="center">')
write('<th colspan="2" bgcolor="#E0E0E0"> <h1> Python %s module attributes and their doc strings </h1></th>' % module)

for attr in dir(mod):
    try:
        write('''
        <tr bgcolor="#FFFFFF">
        <td>%s</td>
        <td>%s</td>
        </tr>
        ''' % (attr, getattr(mod, attr).__doc__.replace('\n','<br>')))
    except:
        pass
write('</table>')
