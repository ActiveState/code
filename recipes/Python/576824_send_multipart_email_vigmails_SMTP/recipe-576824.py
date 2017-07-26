def email_it_via_gmail(headers, text=None, html=None, password=None):
    """Send an email -- with text and HTML parts.
    
    @param headers {dict} A mapping with, at least: "To", "Subject" and
        "From", header values. "To", "Cc" and "Bcc" values must be *lists*,
        if given.
    @param text {str} The text email content.
    @param html {str} The HTML email content.
    @param password {str} Is the 'From' gmail user's password. If not given
        it will be prompted for via `getpass.getpass()`.
    
    Derived from http://code.activestate.com/recipes/473810/ and
    http://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems
    """
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import re
    import smtplib
    import getpass
    
    if text is None and html is None:
        raise ValueError("neither `text` nor `html` content was given for "
            "sending the email")
    if not ("To" in headers and "From" in headers and "Subject" in headers):
        raise ValueError("`headers` dict must include at least all of "
            "'To', 'From' and 'Subject' keys")

    # Create the root message and fill in the from, to, and subject headers
    msg_root = MIMEMultipart('related')
    for name, value in headers.items():
        msg_root[name] = isinstance(value, list) and ', '.join(value) or value
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want
    # to display.
    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)

    # Attach HTML and text alternatives.
    if text:
        msg_text = MIMEText(text.encode('utf-8'), _charset='utf-8')
        msg_alternative.attach(msg_text)
    if html:
        msg_text = MIMEText(html.encode('utf-8'), 'html', _charset='utf-8')
        msg_alternative.attach(msg_text)

    to_addrs = headers["To"] \
        + headers.get("Cc", []) \
        + headers.get("Bcc", [])
    from_addr = msg_root["From"]
    
    # Get username and password.
    from_addr_pats = [
        re.compile(".*\((.+@.+)\)"),  # Joe (joe@example.com)
        re.compile(".*<(.+@.+)>"),  # Joe <joe@example.com>
    ]
    for pat in from_addr_pats:
        m = pat.match(from_addr)
        if m:
            username = m.group(1)
            break
    else:
        username = from_addr
    if not password:
        password = getpass.getpass("%s's password: " % username)
    
    smtp = smtplib.SMTP('smtp.gmail.com', 587) # port 465 or 587
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(username, password)
    smtp.sendmail(from_addr, to_addrs, msg_root.as_string())
    smtp.close()
