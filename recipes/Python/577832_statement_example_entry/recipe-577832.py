#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lintao
import copy

class Entry(object):
    def __init__(self, fields):
        self.__fields = fields
        # Some inner status
        self.__isenableedit = False
        self.__isenablequery = False
        # The really data to save
        self.__realdict = {}

    def getfield(self):
        return self.__fields

    def __getitem__(self, key):
        # keep safe to get item
        if not self.__isenablequery:
            raise Exception, "Please enable query first"
            return
            pass
        if not self.__check_key(key):
            raise Exception, "the Key (%s) is not in the Entry"%repr(key)
        return self.__realdict.get(key, None)
        pass

    def __setitem__(self, key, value):
        # keep safe to set item
        if not self.__isenableedit:
            raise Exception, "Please enable edit first"
            return
        if not self.__check_key(key):
            raise Exception, "the Key (%s) is not in the Entry"%repr(key)
        self.__realdict[key] = value
        pass

    def __check_key(self, key):
        if not key:
            return False
        if isinstance(key, str):
            return (key in self.__fields)
        return all( (i in self.__fields) for i in key)

    # use a dict to update self.__realdict
    def update(self, indict):
        # keep safe to set item
        if not self.__isenableedit:
            raise Exception, "Please enable edit first"
            return
        if not self.__check_key(indict.keys()):
            raise Exception, "the Key (%s) may be not in the Entry"%repr(key)
        self.__realdict.update(indict)
        pass

    def copydict(self):
        return copy.deepcopy(self.__realdict)

    # query
    def enablequery(self):
        if self.__isenablequery:
            return
        self.disableedit()
        self.__isenablequery = True
        pass

    def disablequery(self):
        if not self.__isenablequery:
            return
        self.__isenablequery = False
        pass

    # use with statement
    class __inner_query(object):
        def __init__(self, outer):
            self.outer = outer
        def __enter__(self):
            self.outer.enablequery()
            return self.outer
        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.disablequery()
            #self.outer.test_disp_status()
    def query(self):
        return self.__inner_query(self)

    # ###########################################

    # edit
    def enableedit(self):
        if self.__isenableedit:
            return
        # also to enable query
        self.enablequery()
        self.__isenableedit = True
        pass
        pass

    def disableedit(self):
        if not self.__isenableedit:
            return
        self.__isenableedit = False
        self.disablequery()
        pass
        pass
    # with statement
    class __inner_edit(object):
        def __init__(self, outer):
            self.outer = outer
        def __enter__(self):
            self.outer.enableedit()
            return self.outer
        def __exit__(self, exc_type, exc_value, traceback):
            self.outer.disableedit()
            #self.outer.test_disp_status()
    def edit(self):
        return self.__inner_edit(self)
    # ###########################################

    def test_check_key(self, key):
        return self.__check_key(key)

    def test_disp_status(self):
        print "__isenableedit", self.__isenableedit
        print "__isenablequery", self.__isenablequery
        pass

    pass

if __name__ == '__main__':
    keys = ["id", "name", "age"]
    notkeys = ["not_%s"%i for i in keys]
    oneentry = Entry(keys)
    for i in keys:
        print oneentry.test_check_key(i)
    for i in notkeys:
        print oneentry.test_check_key(i)

    oneentry.enableedit()
    oneentry.test_disp_status()
    oneentry["id"] = 10
    oneentry["name"] = "lintao"
    oneentry["age"] = 22
    oneentry.disableedit()
    oneentry.test_disp_status()

    oneentry.enablequery()
    oneentry.test_disp_status()
    print oneentry["id"]
    print oneentry["name"]
    print oneentry["age"]
    oneentry.disablequery()
    oneentry.test_disp_status()
    # Exception
    #print oneentry["age"]
    #oneentry["name"] = "lintao"

    # with statement
    print "with statement:"
    with oneentry.edit():
        oneentry["id"] = 2
        oneentry["name"] = "lintao51"
        oneentry["age"] = 22
        #oneentry["noage"] = "no"
    with oneentry.query():
        print oneentry["id"]
        print oneentry["name"]
        print oneentry["age"]
        #print oneentry["noage"]

    newdict = {"id":"3","name":"lint","age":"22"}
    with oneentry.edit():
        oneentry.update(newdict)
    with oneentry.query():
        print oneentry["id"]
        print oneentry["name"]
        print oneentry["age"]

    def test_query(entry):
        return entry.query()

    with test_query(oneentry):
        print oneentry["id"]
        print oneentry["name"]
        print oneentry["age"]

    print oneentry.copydict()

    # use class
    #print "use class"

    #class test_query_2(object):
    #    def __init__(self, entry):
    #        self.entry = entry
    #    def __enter__(self):
    #        print "enter in test_query_2"
    #        self.entry.enablequery()
    #        print "self.entry.enablequery"
    #        return self.entry #.query()

    #    def __exit__(self, exc_type, exc_value, traceback):
    #        self.entry.disablequery()
    #        print "self.entry.disablequery"
    #        print "exit from test_query_2"

    #with test_query_2(oneentry) as f:
    #    #with f.query():
    #    print f["id"]




    pass
