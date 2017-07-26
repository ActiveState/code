def toDict(curs):
    """Convert a DBI result to a list of dictionaries."""
    cols = [column[0] for column in curs.description]
    return [dict(zip(cols, row)) for row in curs.fetchall()]

curs.execute('SELECT * FROM mytable')
print toDict(curs)
