def size(bytes=0):
    kbyte = 1024
    mbyte = (kbyte**2)
    gbyte = (kbyte**3)
    tbyte = (kbyte**4)
    pbyte = (kbyte**5)
    ebyte = (kbyte**6)
    zbyte = (kbyte**7)
    
    if bytes < kbyte: 
        retv = '%dB' % int(bytes)
        return unicode('%9s' % retv)
    elif bytes >= kbyte and bytes < mbyte:
        retv = '%04.02fKB' % (float(bytes) / float(kbyte))
        return unicode('%9s' % retv)
    elif bytes >= mbyte and bytes < gbyte:
        retv = '%04.02fMB' % (float(bytes) / float(mbyte))
        return unicode('%9s' % retv)
    elif bytes >= gbyte and bytes < tbyte:
        retv = '%04.02fGB' % (float(bytes) / float(gbyte))
        return unicode('%9s' % retv)
    elif bytes >= tbyte and bytes < pbyte:
        retv = '%04.02fTB' % (float(bytes) / float(tbyte))
        return unicode('%9s' % retv)
    elif bytes >= pbyte and bytes < ebyte:
        retv = '%04.02fPB' % (float(bytes) / float(pbyte))
        return unicode('%9s' % retv)
    elif bytes >= ebyte and bytes < zbyte:
        retv = '%04.02fEB' % (float(bytes) / float(ebyte))
        return unicode('%9s' % retv)
    else:
        retv = '%04.02fZB' % (float(bytes) / float(zbyte))
        return unicode('%9s' % retv)
        
def time(seconds=0):
    # These are for convenience
    minute = 60
    hour   = (minute**2)
    day    = (hour*24)
    week   = (day*7)
    month  = (week*4)
    year   = (month*12)
    
    secs, mins, hrs, days, weeks, months, years = 0, 0, 0, 0, 0, 0, 0
    
    if seconds > year:
        years   = (seconds / year)
        tmp     = (seconds % year)
        seconds = tmp
    if seconds > month:
        months  = (seconds / month)
        tmp     = (seconds % month)
        seconds = tmp
    if seconds > week:
        weeks   = (seconds / week)
        tmp     = (seconds % week)
        seconds = tmp
    if seconds > day:
        days    = (seconds / day)
        tmp     = (seconds % day)
        seconds = tmp
    if seconds > hour:
        hrs     = (seconds / hour)
        tmp     = (seconds % hour)
        seconds = tmp
    if seconds > minute:
        mins    = (seconds / minute)
        secs    = (seconds % minute)
    if seconds < minute:
        secs   = seconds

    if years != 0:
        return unicode('%4dy%2dm%1dw%1dd %02d:%02d:%02d' % (
            years, months, weeks, days, hrs, mins, secs
        ))
    if months != 0:
        return unicode('%2dm%1dw%1dd %02d:%02d:%02d' % (
            months, weeks, days, hrs, mins, secs
        ))
    if weeks != 0:
        return unicode('%1dw%1dd %02d:%02d:%02d' % (
            weeks, days, hrs, mins, secs
        ))
    if days != 0:
        return unicode('%1dd %02d:%02d:%02d' % (days, hrs, mins, secs))
        
    return unicode('%02d:%02d:%02d' % (hrs, mins, secs))
