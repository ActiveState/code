#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao

# TODO
# This may have some bugs.
# So, I need to develop it.

import MySQLdb
from gensql import gensql

import copy

class LoginInfo(object):
    def __init__(self):
        self.user = "lint"
        self.passwd = "123456"
        self.host = "localhost"
        self.db = ""


class Table(object):
    def __init__(self, tablename, logininfo):
        self.tablename = tablename
        self.__login(logininfo)
        self.__describe_table()
        # Variable
        self.__condition__enable = False
        self.__set_condition__enable = False
        pass

    def __login(self, logininfo):
        try:
            self.conn = MySQLdb.connect(
                    host = logininfo.host,
                    user = logininfo.user,
                    passwd = logininfo.passwd,
                    db = logininfo.db)
        except:
            raise Exception, "Login failed"

    def __execute(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)

    def __commit(self):
        self.conn.commit()

    def __describe_table(self):
        sql = "describe %s;" %self.tablename
        self.__execute(sql)
        self.tablekeys = [ i[0] for i in self.cursor.fetchall()]
        pass

    def __check_inputkey(self, inputkey):
        if not inputkey:
            return True
        if isinstance(inputkey, str):
            return (inputkey in self.tablekeys)
        return all((i in self.tablekeys) for i in inputkey)

    def __getitem__(self, key):
        if not self.__condition__enable:
            raise Exception, "Please enable conditions, or in the with statement"
            return
        if not (self.__check_inputkey(key) or key=="*"):
            raise Exception, "Not found the key:(%s)"%key
            return 
        if self.__one_entry:
            if key == "*":
                return self.__one_entry
            return self.__one_entry[key]

    def selectBeginCond(self, conddicts=None):
        """ 
        You need to begin with cond,
        so I can begin to fetch data
        """
        if self.__condition__enable:
            return
        self.__condition__enable = True
        if not self.__check_inputkey(conddicts):
            raise Exception, "The condition has some errors"

        sql = gensql("select", \
                self.tablename, \
                ",".join(self.tablekeys), \
                conddicts)
        self.__execute(sql)
        self.__one_entry = None
        pass

    def selectNext(self):
        if self.__condition__enable:
            tmpone = self.cursor.fetchone()
            if tmpone:
                self.__one_entry = dict(zip(self.tablekeys, \
                        tmpone))
                if self.__one_entry:
                    return True
        return False
        pass

    def selectEndCond(self):
        if not self.__condition__enable:
            return
        self.__condition__enable = False
        self.__one_entry = None
        pass
    # 
    def selectcond(self, cond=None):
        return self.innerselect(self, cond)
    
    # Use the with Statement
    class innerselect(object):
        def __init__(self, outer, cond):
            self.outer = outer
            self.cond = cond
        def __enter__(self):
            self.outer.selectBeginCond(self.cond)
            return self

        def next(self):
            return self.outer.selectNext()

        def __getitem__(self, key):
            return self.outer[key]

        def __getitem__raise(self, *args, **kwds):
            raise Exception, "Can't call out the with statement"

        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.selectEndCond()

    #
    def updatecond(self, cond=None):
        return self.innerupdate(self, cond)

    class innerupdate(object):
        def __init__(self, outer, cond):
            self.outer = outer
            self.cond = cond

        def __enter__(self):
            self.outer.updateBeginCond(self.cond)
            return self

        def next(self):
            return self.outer.updateNext()

        def ok(self):
            self.outer.updateOK()

        def __getitem__(self, key):
            return self.outer[key]

        def __setitem__(self, key, value):
            self.outer[key] = value

        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.updateEndCond()



    # TODO
    def updateBeginCond(self, conddicts):
        if self.__set_condition__enable:
            return
        self.__set_condition__enable = True
        self.selectBeginCond(conddicts)
        # It is to save the conddicts
        self.__tmp__dict__update = copy.deepcopy(conddicts)
        pass

    def updateEndCond(self):
        # if it didn't start, just return
        if not self.__set_condition__enable:
            return
        self.__tmp__dict__update = None
        self.selectEndCond()
        self.__set_condition__enable = False
        pass

    def updateNext(self):
        if not self.__set_condition__enable:
            return False
        return self.selectNext()

    def updateOK(self):
        #print self.__one_entry
        # TODO
        # Really to update
        if not isinstance(self.__one_entry, dict):
            return False
        sql = gensql("update", \
                self.tablename, \
                self.__one_entry, \
                self.__tmp__dict__update)
        self.__execute(sql)
        self.__commit()
        return True
        pass

    def __setitem__(self, key, value):
        if not (self.__condition__enable and self.__set_condition__enable):
            pass
        if not (self.__check_inputkey(key)):
            raise Exception, "Not found the key:(%s)"%key
            return 
        self.__one_entry[key] = value

        pass

    # TODO
    def insertBegin(self):
        if self.__condition__enable or self.__set_condition__enable:
            return 
        self.__condition__enable = True
        self.__set_condition__enable = True
        self.__one_entry = {} #dict((key, None) for key in self.tablekeys)
        pass

    def insertEnd(self):
        if not (self.__condition__enable and self.__set_condition__enable):
            return
        self.__condition__enable = False
        self.__set_condition__enable = False
        if not any(self.__one_entry.values()):
            print "nothing to insert"
            return
        sql = gensql("insert", \
                self.tablename, \
                self.__one_entry)
        self.__execute(sql)
        self.__commit()
        self.__one_entry = None
        pass

    def insertcond(self):
        return self.innerinsert(self)
        pass

    class innerinsert(object):
        def __init__(self, outer):
            self.outer = outer

        def __enter__(self):
            self.outer.insertBegin()
            return self
        def __getitem__(self, key):
            return self.outer[key]

        def __setitem__(self, key, value):
            self.outer[key] = value

        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.insertEnd()

    pass

if __name__ == "__main__":
    logininfo = LoginInfo()
    logininfo.db = "TestBesBkk"
    t = Table("person", logininfo)
    # Test 0
    #print t.tablekeys
    #print t.s__check_inputkey("id_p")
    #print t.s__check_inputkey(["id_p","p"])
    # Test 1
    #t.selectBeginCond({"id_p":2})
    #while t.selectNext():
    #    print t["id_p"], 
    #    print t["name_p"]
    #    print t["*"]
    #    #print t["notexist"]
    #t.selectEndCond()
    #pass
    # Test 2
    #t.updateBeginCond({"id_p":3})
    #while t.updateNext():
    #    #t["id_p"] = "3"
    #    t["id_p"] = "3"

    #    t.updateOK()
    #t.updateEndCond()

    # Post Test 3

    #t.selectBeginCond()
    #while t.selectNext():
    #    print t["id_p"], 
    #    print t["name_p"]
    #    print t["*"]
    #t.selectEndCond()

    # Test 4
    #t.insertBegin()
    #t["id_p"] = 10
    #t.insertEnd()

    # Test 5
    #with t.selectcond() as l:
    #    while l.next():
    #        print l["*"]
    ##print l["*"]

    # Test 6
    #with t.updatecond({"id_p":3}) as l:
    #    while l.next():
    #        l["name_p"] = "lint@ihep"
    #        l["age"] = "222"
    #        l.ok()

    # Test 7
    with t.insertcond() as l:
        l["name_p"] = "lintao51@gmail.com"
        l["id_p"] = 100
        l["age"] = 22
    print l["name_p"]
