def email_it(server, headers, text=None, html=None, password=None):
    """Send an email -- with text and HTML parts.
    
    @param server {str} The SMTP server (e.g. mail.example.com) via which
        to send the email.
    @param headers {dict} A mapping with, at least: "To", "Subject" and
        "From", header values. "To", "Cc" and "Bcc" values must be *lists*,
        if given.
    @param text {str} The text email content.
    @param html {str} The HTML email content.
    
    Derived from <http://code.activestate.com/recipes/576824/>
    """
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import smtplib
    
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
        msg_text = MIMEText(text.encode('utf-8'))
        msg_alternative.attach(msg_text)
    if html:
        msg_text = MIMEText(html.encode('utf-8'), 'html')
        msg_alternative.attach(msg_text)

    to_addrs = headers["To"] \
        + headers.get("Cc", []) \
        + headers.get("Bcc", [])
    from_addr = msg_root["From"]
    
    smtp = smtplib.SMTP(server)
    smtp.sendmail(from_addr, to_addrs, msg_root.as_string())
    smtp.quit()
