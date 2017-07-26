"""
This module can be used to calculate file hashes, store them in a database file
and retrieve them at a later date.

It uses the files modify time stamp to know if it can use the hash stored in
the db or if it has to re-calculate it. So the user will not have to worry
about the hash being incorrect if the file changes in between runs.

usage:
    hdb = HashDB()
    hdb.Load('dbfile.hashdb') # load hashes from db file
    md5 = hdb.Get('somefile', hashtype='md5') # retrieve hash
    hdb.Clean(maxAge=24*60*60) # removes old and invalid entries
    hdb.Write('dbfile.hashdb') # write hashes to db file
"""

__author__ = 'Eysteinn Torfi Kristinsson'
__copyright__ = "Copyright 2012, MIT License"

import hashlib
import cPickle
import os
import time

def CalcFileHash(path, hashtype, buffer=8192):
    '''
    Calculate the hash of a file.
    '''
    hash = getattr(hashlib, hashtype)()
    with open(path, 'rb') as fp:
        while 1:
            data = fp.read(buffer)
            if not data:
                break
            hash.update(data)
    return hash.digest()


class HashDB(object):
    '''
    Calculate and manage file hashes using database files.
    '''

    def __init__(self):
        self.db = {}

    def Load(self, dbFile):
        '''
        Load DB from a file.
        '''
        with open(dbFile, 'rb') as fp:
            self.db.update(cPickle.load(fp))

    def Cleanup(self, maxAge=None):
        '''
        Deletes entries that are no longer valid.
        Checks if file exists and if it has the same modify time stamp, if not
        then the entry is deleted from the DB.
        maxAge (in seconds) can also be passed in, it is used to check against
        the last time the entry was accessed in the DB and if the entry is
        older than maxAge, then it is deleted from the DB.
        '''
        deletes = []
        for path, (mtime, atime, cache) in self.db.iteritems():
            if not os.path.isfile(path) or \
                        (maxAge is not None and atime < time.time()-maxAge) or \
                        mtime != int(os.stat(path).st_mtime):
                deletes.append(path)
        for path in deletes:
            del self.db[path]

    def Get(self, path, hashtype='md5'):
        '''
        Retrieve hash from DB. If not found in the DB or the file has been
        modified since last it's hash was retrieved, a new one will be
        calculated and stored in the DB.
        '''
        # self.db[path][0] is modify time of file
        # self.db[path][1] is access time of db entry
        # self.db[path][2] is dict containing file hashes
        mtime = int(os.stat(path).st_mtime)
        if path in self.db:
            if self.db[path][0] != mtime:
                self.db[path] = [mtime, 0, {}]
            if not hashtype in self.db[path][2]:
                self.db[path][2][hashtype] = CalcFileHash(path, hashtype)
        else:
            self.db[path] = [mtime, 0,
                {hashtype : CalcFileHash(path, hashtype)}]
        self.db[path][1] = time.time() # update access time
        return self.db[path][2][hashtype]

    def Write(self, dbFile):
        '''
        Write DB to file.
        '''
        with open(dbFile, 'wb') as fp:
            cPickle.dump(self.db, fp)


def test():
    import sys, tempfile, shutil
    startTime = time.time()
    testfolder = '.'
    dbFile = 'data.hashdb'
    hdb = HashDB()
    if os.path.isfile(dbFile):
        print 'Loading from file'
        hdb.Load(dbFile)
    try:
        for root, dirs, files in os.walk(testfolder):
            for fileName in files:
                fileAbs = os.path.abspath(os.path.join(root, fileName))
                if os.path.isfile(fileAbs):
                    hashtype = 'sha1'
                    print '%s (%s): %r' % (
                        fileAbs, 
                        hashtype, 
                        hdb.Get(fileAbs, hashtype),
                        )
    finally:
        print 'Cleaning DB'
        hdb.Cleanup(60*30) # 30 minutes
        print 'writing to file'
        # incase KeyboardInterrupt, write to tempfile so we don't destroy
        # the database we had previously 
        dbFilePath, dbFileName = os.path.split(dbFile)
        tmpFile = tempfile.mktemp(
            dir = dbFilePath,
            prefix = dbFileName+'_',
            suffix='.tmp',
            )
        try:
            hdb.Write(tmpFile)
            shutil.move(tmpFile, dbFile)
        except:
            os.unlink(tmpFile)
            raise
    td = time.time()-startTime
    print td
    print 'total runtime: %dm%02ds' % (td/60, td%60)

if __name__ == '__main__':
    test()
