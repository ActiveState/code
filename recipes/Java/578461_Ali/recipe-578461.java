## {{{ http://code.activestate.com/recipes/578439/ (r1)
#Just a try using the thread modules.


import urllib as ul
import bs4 as bs
import urlparse as up
import re as re 
import os.path as op 
import Queue as que
import time
import threading

pat = re.compile('.*[\d]{4,7}.*')

count=0

class dldfile(threading.Thread):
    def __init__(self,qu1):
        threading.Thread.__init__(self)
        self.qu1=qu1
        self.ad='download/1/'
        
    def run(self):
        try:
            url,filename=self.qu1.get()
            url =url+self.ad             #comment this line in case need to download whole web page instead of recipe ONLY...
            ul.urlretrieve(url,filename)
            global count
        except:
            print " RE-TRYING ",
            count= count - 1
            self.qu1.put((url,filename))
            self.run()
        finally:
            count= count +1
            print str(count)+"("+str( threading.activeCount())  +")",filename
            self.qu1.task_done()

class dload(threading.Thread ):
    def __init__(self,qu,url = "http://code.activestate.com/recipes/langs/python/?page=" ):
        threading.Thread.__init__(self)
        self.url=  url
        self.q =que.Queue()
        self.qu=qu
        
    def run(self):
        ind=self.qu.get()
        url=self.url+str(ind)
        soup =bs.BeautifulSoup(''.join( ul.urlopen(url).readlines() ))
        bu = up.urlsplit(self.url)
        print 'started with the ' ,str(url).split('/')[-1],
        for i in  soup.find_all(attrs = { "class" : "recipe-title"}):
            sp = up.urlsplit(i.a.get('href'))
            path = sp.path
            print path
            if re.search(pat, path):
                path = bu.scheme+'://'+bu.netloc+path
                filename = str(path).split('/')[-2]
                filename = op.join(op.abspath(op.curdir),filename+'.py') # recipe will be stored in given location
#                filename = op.join(op.abspath(op.curdir),filename+'.html')
#uncomment the above line if downloading the web page for teh recipe
                print path
                self.q.put((path,filename))
        self.fetch_data()
        time.sleep(1)
        self.qu.task_done()
        self.q.join()
        print 'done with the ' ,str(url).split('/')[-1],
        
    def fetch_data(self):
        Que1 = que.Queue()
        minitask =10
        while not self.q.empty():
            for i in range(minitask):
                x = dldfile(Que1)
                x.setDaemon(True)
                x.start()
            for j in range(minitask):
                Que1.put(self.q.get())
            Que1.join()
            del x

if __name__ =='__main__':
    task=5
    Que = que.Queue()
    for k in range(1,190,task):  # no. of pages included under the python tag.  188 is current count and 3700+ python recipes
        print "\n PAGE # : {0} \t \nDeploying  Fresh threads\n".format(k)
        for i in range(task):
            t = dload(Que)
            t.start()
        for j in range(task):
            Que.put(k+j)
        Que.join()
        Que.queue.clear()
        del t
        print "DONE\n"
        time.sleep(2)
    del Que
    print "Our buisness finished"
## end of http://code.activestate.com/recipes/578439/ }}}
