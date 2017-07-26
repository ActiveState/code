def fields(cursor):
    '''
    This fuction takes a DB API 2.0 cursor object that has been executed and returns a dictionary of the field names and column numbers.  Field names are the key, column numbers are the value.
    This lets you do a simple cursor_row[field_dict[fieldname]] to get the value of the column.
    Returns dictionary
    '''
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1

    return results       
