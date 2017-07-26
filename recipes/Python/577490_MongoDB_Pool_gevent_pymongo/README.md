## MongoDB Pool for gevent and pymongo packages  
Originally published: 2010-12-08 07:51:27  
Last updated: 2011-09-02 05:56:58  
Author: Andrey Nikishaev  
  
Wrote some simple implementation of pool for pymongo package under gevent coroutine library.

Base bug here was with pymongo.connection.Pool because in the original package it is thread-local, so when you spawn new greenlet and trying to get already open connection, it creates new connection because in this greenlet pool is empty. So if you will implement your own pool don’t forget about this.

#Example of use:
    # Create Pool. 
    db = Mongo('test_db',10)
    # Get connection from pool
    conn = db.get_conn()
    # Get raw connection for GridFS
    raw_conn = conn.getDB

    #Mongo is a singleton. So if you want to get connection in another part of application just type
    db = Mongo()
    conn = db.get_conn()

    #Connection will get back to pool when context will be closed.