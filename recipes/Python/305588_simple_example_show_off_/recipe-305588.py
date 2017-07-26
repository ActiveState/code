#there are all sorts of iterable objects in python nowadays
#for example, you can use itertools.tee on these:
iterable_obj=[1,2,3] #list
iterable_obj=( i for i in (1,2,3) ) #py 2.4 generator
iterable_obj=open('a.txt') #file handle
iterable_obj=os.popen('ls') #process to get dir listing

#also for an iterable function
def iterable_func():
    for i in (1,2,3): yield i

#create 2 iterators
iterators = itertools.tee(iterable_obj)
#or for a function
iterators= itertools.tee(iterable_func())

#notice that you now have 2 iterable objects
print iterators
>>> (<itertools.tee object at 0x0089E040>, <itertools.tee object at 0x0089E050>)

#create 5 iterators
iterators=itertools.tee(iterable_obj,5)


###here is a trivial program that uses 2 iterators, where one iterator
###stays behind the other and advances on certain commands 
import itertools

Saved=[]
Compressed=[]
def get_data():
    data=['a.gif','b.gif','c.gif','save','e.gif','save']
    data+=['f.gif','compress','g.gif','h.gif','i.gif','save']
    for i in data: yield i

def display(image): print 'displaying',image

def move_to_present(history_it,action):
    print '*Now doing action',action
    for item in history_it:
        if item in ('save','compress','reset'): break
        if action=='save':
            Saved.append(item)
        elif action=='compress':
            Compressed.append(item)
        #reset just allows the iterator to move back to the front
        #no other action needed

#make 2 iterators, it_history stays behind and moves forward
#whenever 'save' or 'compress' is received
it_main,it_history =itertools.tee(get_data())


for item in it_main:
    if item in ('save','compress','reset'):
        #move the history iterator forward to 
        #last iterator item displayed
        move_to_present(it_history,item)
    else:
        display(item)
    
print 'Saved',Saved
print 'Compressed and Saved',Compressed

#running this results in:
>>> displaying a.gif
displaying b.gif
displaying c.gif
*Now doing action save
displaying e.gif
*Now doing action save
displaying f.gif
*Now doing action compress
displaying g.gif
displaying h.gif
displaying i.gif
*Now doing action save
Saved ['a.gif', 'b.gif', 'c.gif', 'e.gif', 'g.gif', 'h.gif', 'i.gif']
Compressed and Saved ['f.gif']
