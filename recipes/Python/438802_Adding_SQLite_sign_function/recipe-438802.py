def _sign(val):
    if val:
        if val > 0: return 1
        else: return -1
    else:
        return val

#get your db connection, conn
conn.create_function("sign", 1, _sign)

...

>>cur = c.conn.cursor()
>>cur.execute("select test, val from test")
>>cur.fetchall()
[(u'a', None)]

>>cur.execute("select sign(test), sign(val), sign(0), sign(-99), sign(99) from test")
>>cur.fetchall()
[(1, None, 0, -1, 1)]
