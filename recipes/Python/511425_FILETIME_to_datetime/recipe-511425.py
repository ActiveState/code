import datetime

_FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
def FiletimeToDateTime(ft):
    timestamp = ft.dwHighDateTime
    timestamp <<= 32
    timestamp |= ft.dwLowDateTime
    return _FILETIME_null_date + datetime.timedelta(microseconds=timestamp/10)
