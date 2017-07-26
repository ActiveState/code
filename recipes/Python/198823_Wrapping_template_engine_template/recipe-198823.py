def render(template, script, **kargs):  

    funcname = 'execute_render'
    varlist = []
    for key in kargs.keys():
        varlist.append("%s = globals()['%s']" % (key, key))
    kargs['__template__'] = template

    # Generate a function so run with template code.
    funccode = compile(
        'def %s():\n' % funcname
        # Assign to local variables.
        + '%s\n' % '\n'.join(map(lambda s: ' %s' % s, varlist))
        # One level indent
        + '%s\n' % '\n'.join(map(lambda s: ' %s' % s, script.split('\n'))),
        funcname, 'exec')
    # Generate a function and execution.
    eval(funccode, kargs, locals())
    return eval('%s()' % funcname)

def test():
    src = '''
import tinpy
return tinpy.build(__template__, vals=header_dict)
'''
    tpl = """\
Date: [% var vals['datetime'] %]
From: [% var vals['fromaddr'] %]
To: [% var vals['toaddr'] %]    
Subject: Test mail

This is a test mail.
"""

    import time
    import smtplib
    
    header_dict = {
        'datetime': time.strftime('%a, %d %b %Y %T %z'),
        'fromaddr': 'from@example.com',
        'toaddr': 'to@example.com'}

    maildata = render(tpl, src, header_dict=header_dict)
    server = smtplib.SMTP('localhost')
    server.sendmail(
        header_dict['fromaddr'], [header_dict['toaddr']],
        maildata.replace('\n', '\r\n'))
    server.quit()

test()
