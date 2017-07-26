from datetime import datetime
from email.utils import parsedate

def _parse_http_datetime(s):
    return datetime(*parsedate(s)[:6])
