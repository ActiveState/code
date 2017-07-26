def get_ip(ip=None):
    """Attempt to get user's IP address (even behind a proxy), return None if no go.

    >>> get_ip('123.234.123.234')
    '123.234.123.234'
    >>> get_ip('1.2.3.4, 4.3.2.1')
    '1.2.3.4'
    >>> get_ip('1.2.3.4, unknown')
    '1.2.3.4'
    >>> get_ip('1.2.3.4, 4.3.2.1, 5.6.7.8')
    '1.2.3.4'
    >>> get_ip('172.22.23.64 , 192.168.255.30, 146.79.254.10')
    '172.22.23.64'
    >>> get_ip('unknown, 1.2.3.4')
    '1.2.3.4'
    >>> get_ip('a, b, 1.2.3.4')
    '1.2.3.4'
    >>> print get_ip('asdf')
    None
    >>> print get_ip('')
    None
    >>> print get_ip('256.1.1.1')
    None

    """
    if ip is None:
        ip = web.ctx.env.get('HTTP_X_FORWARDED_FOR', web.ctx.get('ip', ''))

    # Grab the first valid IP address in the "1.2.3.4, 4.3.2.1, ..." format (this is the
    # format of the X-Forwarded-For header)
    for ip in ip.split(','):
        ip = ip.strip()
        try:
            socket.inet_aton(ip)
            return ip
        except socket.error:
            pass

    # No go, bad format
    return None
