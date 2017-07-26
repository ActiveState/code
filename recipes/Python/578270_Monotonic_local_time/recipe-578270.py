import time

def monotoniclocaltime(seconds=None):
    """monotoniclocaltime([seconds]) -> (tm_year,tm_mon,tm_mday,tm_hour,tm_min,
                                  tm_sec,tm_wday,tm_yday,tm_isdst)

Convert seconds since the Epoch to a time tuple expressing monotonic
local time. Monotonicity is achieved by extending the day before the
end of DST with some extra hours (24, 25 etc) until after the switch."""

    if seconds is None:
        seconds = time.time()

    res = time.localtime(seconds)

    dayseconds = res.tm_sec + res.tm_min*60 + res.tm_hour*3600
    nextmidnight = time.localtime(seconds - dayseconds + 86400)

    if res.tm_isdst and not nextmidnight.tm_isdst:
        tl = list(time.localtime(seconds - 86400))  # same time yesterday
        tl[3] += 24                                 # plus 24h
        res = time.struct_time(tl)

    return res

def test():

    def findswitch():
        start = (int(time.time()) // 86400) * 86400
        for t in range(start, start + 365*86400, 3600):
            if monotoniclocaltime(t) != time.localtime(t):
                return t

    def iso8601(tup):
        return "%04d-%02d-%02d %02d:%02d:%02d" % tuple(tup)[:6]

    switch = findswitch()
    if not switch:
        print("No time zone transitions found in your local timezone")
        return

    for t in range(switch-3600*5, switch+3600*5, 3600):
        print(iso8601(monotoniclocaltime(t-1)))
        print(iso8601(monotoniclocaltime(t)))

if __name__ == '__main__':
   test()
