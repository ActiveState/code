import MySQLdb

# Create a connection object and create a cursor
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="joe", passwd="egf42" db="tst")
Cursor = Con.cursor()

# Make SQL string and execute it
sql = "SELECT * FROM Users"
Cursor.execute(sql)

# Fetch all results from the cursor into a sequence and close the connection
Results = Cursor.fetchall()
Con.close()
