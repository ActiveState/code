#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

import MySQLdb
from gensql import gensql
from Entry import Entry

class Error(Exception):
    pass


class SQLAction(object):

    def __init__(self, logininfo):
        self.__login(logininfo)
        self.__entryies = {}
        self.cursor = {}

    def __login(self, logininfo):
        try:
            self.conn = MySQLdb.connect(
                    **logininfo)
        except:
            raise Error,"Login failed"

    def execute(self, sql, tablename):
        self.cursor[tablename] = self.conn.cursor()
        self.cursor[tablename].execute(sql)

    def commit(self):
        self.conn.commit()

    def __describe(self, tablename):
        sql = "describe %s;"%tablename
        self.execute(sql, tablename)
        return list(i[0] for i in self.cursor[tablename].fetchall())
        pass

    # Begin with statement, select
    def select(self, tablename, conddicts=None):
        return self.innerSelect(self, tablename, conddicts)

    class innerSelect(object):
        def __init__(self, outer, tablename, cond=None):
            self.outer = outer
            self.tablename = tablename
            self.cond = cond
            self.entry = self.outer.getentry(self.tablename)
            self.select()

        def select(self):
            sql = gensql("select", \
                    self.tablename, \
                    self.entry.getfield(), \
                    self.cond)
            #print sql
            self.outer.execute(sql, self.tablename)
            pass

        def next(self):
            tmpone = self.outer.cursor[self.tablename].fetchone()
            if not tmpone:
                return False
            with self.entry.edit():
                self.entry.update(dict(zip(self.entry.getfield(), tmpone)))
            self.entry.enablequery()
            return True

        def __enter__(self):
            self.entry.enablequery()
            return self
            pass
        def __getitem__(self, key):
            return self.entry[key]
        def __setitem__(self, key, value):
            raise Error, "Can't set key and value"
        def __exit__(self, exc_type, exc_value, traceback):
            self.entry.disablequery()
            pass
    # End with statement, select

    # Begin with statement, update
    def update(self, tablename, conddicts):
        return self.innerUpdate(self, tablename, conddicts)

    class innerUpdate(object):
        def __init__(self, outer, tablename, cond):
            self.outer = outer
            self.tablename = tablename
            self.cond = cond
            self.entry = self.outer.getentry(self.tablename)
            self.select()
        def __getitem__(self, key):
            return self.entry[key]
        def __setitem__(self, key, value):
            self.entry[key] = value

        def select(self):
            sql = gensql("select", \
                    self.tablename, \
                    self.entry.getfield(), \
                    self.cond)
            #print sql
            self.outer.execute(sql, self.tablename)
            pass

        def next(self):
            tmpone = self.outer.cursor[self.tablename].fetchone()
            if not tmpone:
                return False
            with self.entry.edit():
                self.entry.update(dict(zip(self.entry.getfield(), tmpone)))
            self.entry.enableedit()
            self.oldentry = self.entry.copydict()
            return True

        def update(self):
            sql = gensql("update", \
                    self.tablename, \
                    self.entry.copydict(), \
                    self.oldentry)
            self.outer.execute(sql, self.tablename)
            self.outer.commit()
            pass
        def ok(self):
            self.update()

        def __enter__(self):
            self.entry.enableedit()
            return self
            pass
        def __exit__(self, exc_type, exc_value, traceback):
            self.entry.disableedit()
            pass
    # End with statement, update


    # Begin with statement, insert
    def insert(self, tablename):
        return self.innerInsert(self, tablename)

    class innerInsert(object):
        def __init__(self, outer, tablename):
            self.outer = outer
            self.tablename = tablename
            self.entry = self.outer.getentry(self.tablename)

        def __enter__(self):
            self.entry.enableedit()
            return self
            pass

        def __getitem__(self, key):
            return self.entry[key]
        def __setitem__(self, key, value):
            self.entry[key] = value

        def ok(self):
            self.insert()
        def insert(self):
            sql = gensql("insert", \
                    self.tablename, \
                    self.entry.copydict())
            self.outer.execute(sql, self.tablename)
            self.outer.commit()


        def __exit__(self, exc_type, exc_value, traceback):
            self.entry.disableedit()
            pass
    # End with statement, insert

    def newentry(self, tablename):
        self.__entryies[tablename] = Entry(self.__describe(tablename))

    def getentry(self, tablename):
        return self.__entryies.get(tablename, None)

if __name__ == "__main__":
    logininfo = {"user":"lint", "host":"localhost", "passwd":"123456", "db":"TestBesBkk"}
    sqlaction = SQLAction(logininfo)
    sqlaction.newentry("person")
    oneentry = sqlaction.getentry("person")
    #with oneentry.edit():
    #    oneentry["id_p"] = "5"
    #    oneentry["name_p"] = "lint07"
    #    oneentry["age"] = 22

    #with oneentry.query():
    #    print oneentry["id_p"]
    #    print oneentry["name_p"]
    #    print oneentry["age"]
    #print sqlaction.cursor
    #with sqlaction.insert("person") as s:
    #    s["id_p"] = 1000
    #    s["name_p"] = "lintao07"
    #    s["age"] = 22222
    #    s.ok()
    with sqlaction.update("person", {"id_p":1000}) as s:
        while s.next():
            s["name_p"] = s["name_p"] + str(s["age"])
            s["age"] = 55555
            s.ok()


    #with sqlaction.select("person", None) as s:
    #    print s.entry.getfield()
    #    while s.next():
    #        print s["id_p"]
    #        print s["name_p"]
    #        print s["age"]
    #        #print s["noage"]
