# ---------------------------------------------------------------
def createMail(sender, recipient, subject, html, text):
    '''
    A slightly modified version of Recipe #67083, included here 
    for completeness
    '''
    import MimeWriter, mimetools, cStringIO
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    writer.addheader("From", sender)
    writer.addheader("To", recipient)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")

    pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg

# ---------------------------------------------------------------
def sendMail(sender, recipient, subject, html, text):
    import smtplib
    message = createMail(sender, recipient, subject, html, text)
    server = smtplib.SMTP("localhost")
    server.sendmail(sender, recipient, message)
    server.quit()

# ---------------------------------------------------------------
def main():
    '''
    the main body of your program
    '''
    print x # will raise an exception


# ---------------------------------------------------------------
if __name__ == '__main__':
    try:
        main()
    except:
        import sys, cgitb
        sendMail('bugs@yourdomain.com',
                'webmaster@yourdomain.com',
                'Error on yourdomain.com',
                cgitb.html(sys.exc_info()),
                cgitb.text(sys.exc_info()))

        # handle the error gracefully, perhaps doing a
        # http redirect if this is a cgi application or
        # otherwise letting the user know something happened
        # but that, hey, you are all over it
