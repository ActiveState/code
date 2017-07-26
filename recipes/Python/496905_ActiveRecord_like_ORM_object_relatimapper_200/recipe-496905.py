# this is storm.py
import string, new, MySQLdb
from types import *
from MySQLdb.cursors import DictCursor

bag_belongs_to, bag_has_many = [],[]
def belongs_to(what): bag_belongs_to.append(what)
def has_many(what): bag_has_many.append(what)

class Mysqlwrapper:
        def __init__(self,**kwds):
                self.conn = MySQLdb.connect(cursorclass=DictCursor,**kwds)
                self.cursor = self.conn.cursor()
                self.escape = self.conn.escape_string
                self.insert_id = self.conn.insert_id
                self.commit = self.conn.commit
                self.q = self.cursor.execute

        def qone(self,query):
                self.q(query)
                return self.cursor.fetchone()

        def qall(self,query):
                self.q(query)
                return self.cursor.fetchall()

class MetaRecord(type):
        def __new__(cls, name, bases, dct):
                global bag_belongs_to, bag_has_many
                if name in globals(): return globals()[name]
                else:
                        Record = type.__new__(cls, name, bases, dct)
                        for i in bag_belongs_to: Record.belongs_to(i)
                        for i in bag_has_many: Record.has_many(i)
                        bag_belongs_to = []
                        hag_has_many = []
                        return Record

class Storm(dict):
        __metaclass__ = MetaRecord
        __CONN = None

        @classmethod
        def belongs_to(cls, what):
                def dah(self):
                        belong_cls = globals().get(what,None)
                        if not belong_cls:
                                belong_cls = type(what,(Storm,),{})
                        return belong_cls.selectone(self[what+'_id'])
                setattr(cls,what,new.instancemethod(dah,None,cls))

        @classmethod
        def has_many(cls, what):
                def dah(self):
                        hasmany_cls = globals().get(what,None)
                        if not hasmany_cls:
                                hasmany_cls = type(what,(Storm,),{})
                        dct={}
                        dct[string.lower(cls.__name__)+'_id']=self['id']
                        return hasmany_cls.select(**dct)
                setattr(cls,what,new.instancemethod(dah,None,cls))

        @classmethod
        def conn(cls, **kwds):
                if not cls.__CONN: cls.__CONN = Mysqlwrapper(**kwds)

        @classmethod
        def exe(cls,s):
                if not cls.__CONN: raise "Database not connected"
                return cls.__CONN.qall(s)

        @classmethod
        def insert(cls,**kwds):
                vs = [[k,cls.__CONN.escape(str(kwds[k]))] for k in kwds]
                if vs:
                        s = "insert into %s (%s) values ('%s')" % (
                          string.lower(cls.__name__), ','.join([v[0] for v in vs]),
                          "','".join([v[1] for v in vs]))

                        cls.__CONN.q(s)
                        cls.__CONN.commit()
                        return cls.__CONN.insert_id()
                else: raise "nothing to insert"

        @classmethod
        def select(cls,*args, **kwds):
                if len(args)==1 and (type(args[0])==IntType or type(args[0])==LongType):
                        q = "select * from %s where id='%s'"%(string.lower(cls.__name__),args[0])
                        where = "where id='%s'"%args[0]
                else:
                        if args: s = ",".join(args)
                        else: s = "*"

                        if kwds:
                                c,limit,orderby = [],'',''
                                for k in kwds:
                                        if k == 'limit': limit = "limit "+str(kwds[k])
                                        elif k == 'order': orderby = "order by "+str(kwds[k])
                                        else: c.append(k+"='"+str(kwds[k])+"'")
                                where = " and ".join(c)
                                if where: where = "where %s"%where
                                where = "%s %s %s"%(where,orderby,limit)
                        else: where = ""

                        q = " ".join(['select',s,'from',string.lower(cls.__name__),where])

                r = cls.__CONN.qall(q)
                list = []
                for i in r:
                        list.append(cls(i))
                        list[-1].__dict__['where'] = where
                return list

        @classmethod
        def selectone(cls,*args, **kwds):
                r = cls.select(*args,**kwds)
                if r: return r[0]
                else: return {}

        @classmethod
        def update(cls,cond,**kwds):
                if not cond or not kwds: raise "Update What?!"
                if type(cond) == IntType: w = "id='%d'" % cond
                else: w = cond
                vs = [[k,cls.__CONN.escape(str(kwds[k]))] for k in kwds]
                if vs:
                        s = "UPDATE %s SET %s WHERE %s" % ( string.lower(cls.__name__),
                          ','.join(["%s='%s'"%(v[0],v[1]) for v  in vs]), w)
                        cls.__CONN.q(s)
                        cls.__CONN.commit()

        @classmethod
        def delete(cls,id):
                if type(id) == IntType:
                        cls.__CONN.q("delete from %s where id='%d'"%
                          (string.lower(cls.__name__),id))
                        cls.__CONN.commit()
                else: raise "Only accept integer argument"

        def __init__(self,dct={}):
                if not self.__class__.__CONN: raise "Database not connected"
                dict.__init__(self,dct)
                self.__dict__['cur_table']= string.lower(self.__class__.__name__)
                self.__dict__['where']= ''
                self.__dict__['sql_buff']={}

        def sql(self,sql): self.__class__.__CONN.q(sql)

        def save(self):
                s = ""
                if self.where:
                        f = []
                        for v in self.sql_buff:
                                f.append("%s='%s'"%(v,self.sql_buff[v]))
                        s = "UPDATE %s SET %s %s" % (
                          self.cur_table, ','.join(f), self.where)
                else:
                        f,i=[],[]
                        for v in self.sql_buff:
                                f.append(v)
                                i.append(self.sql_buff[v])
                        if f and i:
                                s = "INSERT INTO %s (%s) VALUES ('%s')" % (
                                  self.cur_table, ','.join(f), "','".join(i))

                if s:
                        self.__class__.__CONN.q(s)
                        self.__class__.__CONN.commit()
                else: raise "nothing to insert"


        def __setattr__(self,attr,value):
                if attr in self.__dict__: self.__dict__[attr]=value
                else:
                        v = self.__class__.__CONN.escape(str(value))
                        self.__dict__['sql_buff'][attr] = v
                        self[attr] = v

        def __getattr__(self,attr):
                if attr in self.__dict__: return self.__dict__[attr]
                try: return self[attr]
                except KeyError: pass
                raise AttributeError

__all__ = ['Storm', 'belongs_to', 'has_many']
#----------------- end of storm.py ----------------


Below is a session screenshot of using this ORM(Storm):
-------------------------------------------------------------
wang@dapper-03:~/spark/lib$ mysql -u root
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 46 to server version: 5.0.22-Debian_0ubuntu6.06-log
Type 'help;' or '\h' for help. Type '\c' to clear the buffer.
mysql> create database teststorm;
Query OK, 1 row affected (0.00 sec)
mysql> use teststorm;
Database changed
mysql> create table author(id int auto_increment primary key,name varchar(50));
Query OK, 0 rows affected (0.06 sec)
mysql> create table book(id int auto_increment primary key,author_id int,title varchar(100));
Query OK, 0 rows affected (0.01 sec)
mysql> describe author;
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(50) | YES  |     | NULL    |                |
+-------+-------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)
mysql> describe book;
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| author_id | int(11)      | YES  |     | NULL    |                |
| title     | varchar(100) | YES  |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
mysql> Bye
wang@dapper-03:~/spark/lib$ python
Python 2.4.3 (#2, Apr 27 2006, 14:43:58)
[GCC 4.0.3 (Ubuntu 4.0.3-1ubuntu5)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from storm import *
>>> class Author(Storm):
...     has_many('book')
...
>>> class Book(Storm):
...     belongs_to('author')
...
>>> Storm.conn(user='root',db='teststorm')
>>> a = Author()
>>> a.name = 'Tolstoy'
>>> a.save()
>>> Author.insert(name='Charles Dickens')
0L
>>> a.name, a['name']
('Tolstoy', 'Tolstoy')
>>> o = Author.selectone(2)
>>> o
{'id': 2L, 'name': 'Charles Dickens'}
>>> o.id, o.name, o['id'], o['name']
(2L, 'Charles Dickens', 2L, 'Charles Dickens')
>>> b = Book()
>>> b.author_id = 1
>>> b.title = 'Anna Karenina'
>>> b.save()
>>> b.title = 'War and Peace'
>>> b.save()
>>> b.author_id = 2
>>> b.title = 'Great Expectations'
>>> b.save()
>>> Book.insert(author_id=2,title='A Tale of Two Cities')
0L
>>> Book.insert(author_id=2,title='David Copperfield')
0L
>>> all = Book.select()
>>> all
[{'author_id': 1L, 'id': 1L, 'title': 'Anna Karenina'}, {'author_id': 1L, 'id': 2L, 'title': 'War and Peace'}, 
{'author_id': 2L, 'id': 3L, 'title': 'Great Expectations'}, {'author_id': 2L, 'id': 4L, 'title': 
'A Tale of Two Cities'}, {'author_id': 2L, 'id': 5L, 'title': 'David Copperfield'}]
>>> o = Book.selectone(4)
>>> a = o.author()
>>> a
{'id': 2L, 'name': 'Charles Dickens'}
>>> a = Author.selectone(name='Tolstoy')
>>> a
{'id': 1L, 'name': 'Tolstoy'}
>>> b = a.book()
>>> b
[{'author_id': 1L, 'id': 1L, 'title': 'Anna Karenina'}, {'author_id': 1L, 'id': 2L, 'title': 'War and Peace'}]
>>> b[0].title, b[1].title
('Anna Karenina', 'War and Peace')
>>>
wang@dapper-03:~/spark/lib$
