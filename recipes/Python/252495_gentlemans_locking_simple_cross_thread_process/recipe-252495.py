Usage example:
#test locking
import glock
file='lock.txt'
l=glock.lock(file)

#do something
time.sleep(60)
#extend the lock
l=glock.lock(file)

##do something again
time.sleep(60)

#now unlock
l.unlock()


###glock
import os,time

class lock:
    '''cross-platform locking.
    Locking will raise exceptions.
    Unlocking won't. So, unlock all you want'''
    def __init__(self,*args,**kwds):
        if not len(args): raise 'need a lock name'
        #detemine how long to wait for locks(min)
        if 'wait' in kwds:
            self.wait=kwds['wait']*60
        else:
            self.wait=300
        name=args[0]
        self.d=name+'_lock/'
        self.d2=name+'_lock2/'
        self.locked={}
        lock_successful=0
        if self.locked.has_key(self.d2):
            try:
                #you got a lock, it is yours?
                if os.stat(self.d2)[8]==\
                   self.locked.get(self.d2):
                    #try to extend lock before loss
                    #ATOMIC operation, extend may
                    #fail, presence of self.d will
                    #prevent loss of lock
                    #just by the act of extending
                    os.rmdir(self.d2)
                    os.mkdir(self.d2)
                    os.rmdir(self.d)
                    os.mkdir(self.d)
                    self.locked[self.d2]=\
                        os.stat(self.d2)[8]
                    lock_successful=1
                if self.locked.has_key(self.d2):
                    del(self.locked[self.d2])
                result='Fail: lost lock'
            except:
                if self.locked.has_key(self.d2):
                    del(self.locked[self.d2])
                result='Fail: lost lock'
        else:
            for t in range(0,self.wait): #try 10 times 
                #not locked yet, try to lock it
                try:
                    os.mkdir(self.d) #ATOMIC  
                    os.mkdir(self.d2) #ATOMIC 
                    self.locked[self.d2]=\
                        os.stat(self.d2)[8]
                    lock_successful=1
                    break
                except Exception,error:
                    result=error
                    print 'locking??',error
                    #mkdir probably failed
                    #lock already there,
                    #try to delete old lock
                    m_dir2=0;m_dir=0
                    if os.path.exists(self.d):
                        try:
                            m_dir2=os.stat(self.d2)[8]
                        except:
                            pass
                        try:
                            m_dir=os.stat(self.d)[8]
                        except:
                            pass
                        cur_tm=int(time.time())
                        #presence of either directory
                        #can stop you from taking lock
                        if cur_tm>m_dir+self.wait and\
                           cur_tm>m_dir2+self.wait:
                            #delete old locks
                            #ATOMIC here
                            os.rmdir(self.d2)
                            os.mkdir(self.d2) 
                            os.rmdir(self.d)
                            os.mkdir(self.d)
                            self.locked[self.d2]=\
                                os.stat(self.d2)[8]
                            lock_successful=1 
                            break
                time.sleep(1)
        #made it thru the loop, so we got no lock
        if not lock_successful:
            raise result
    def unlock(self):
        '''does not raise an exception,
        safe to unlock as often as you want
        it may just do nothing'''
        if self.locked.has_key(self.d2):
            #we're the ones that unlocked it,
            #if time matched
            if self.locked[self.d2]==\
               os.stat(self.d2)[8]:
                try:
                    del(self.locked[self.d2])
                    os.rmdir(self.d2)
                    os.rmdir(self.d)
                    return 1
                except:
                    return 0
            else:
                del(self.locked[self.d2])
            return 0
        else:
            return 0
        
if __name__ == "__main__":
    print 'testing lock'
    file='fred.txt'
    l=lock(file)
    f=open(file,'w')
    f.write('test')
    f.close()
    l.unlock()
