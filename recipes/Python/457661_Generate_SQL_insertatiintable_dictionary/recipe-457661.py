def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql

def dictValuePad(key):
    return '%(' + str(key) + ')s'

def exampleOfUse():
    import MySQLdb
    db = MySQLdb.connect(host='sql', user='janedoe', passwd='insecure', db='food') 
    cursor = db.cursor()
    insert_dict = {'drink':'horchata', 'price':10}
    sql = insertFromDict("lq", insert_dict)
    cursor.execute(sql, insert_dict)
