#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 27/06/08
#Version :2.4
import operator
class Container:
    def __init__(self,switch):    #Initialize
       self.switch = switch
       self.value = [] 
       for item in switch:
           self.value.append(item)
    def append(self,node):
       return self.value.append(node)
    def __getattr__(self,name):
        if name == 'union':
           self.union = operator.or_
           return operator.attrgetter(name)
        elif name == 'intersect':
           self.intersect = operator.and_
           return operator.attrgetter(name)
        else :
             return getattr(self.value,name)
    def __getitem__(self,i):
       return self.switch[i]
    def __len__(self):            # Container length
       return len(self.switch)
    def __and__(self,other):      # Intersection 
       self.intersect = operator.and_
       res = []
       for item in self.switch:
		if item in other:
		    res.append(item)
       return Container(res)
    def __or__(self,other):       # Union
        self.union = operator.or_
	res = self.value[:]
        for item in other:
		if item not in res:
		    res.append(item)
        return Container(res)
    def insideout(self,other):     # !=Intersection != Union item only in x but not in y
        res = []
        for item in self.switch:
            if item not in other:
                res.append(item)
        return Container(res)
    def outinside(self,other):     # != Union != Intersection item in x and y but not in both
        res = []
        for item in self.switch:
            if item not in other:
                res.append(item)
        for item in other:
            if item not in self.switch:
                res.append(item)
        return Container(res)
    def __str__(self):             #Print
        return '<Container : %s \n<Length : %s' % (self.value,(len(self.switch)))

if __name__ == '__main__':
    X = Container([1,2,3,4,5,6])
    Y = Container([3,4,5,6,7,8,0])
    Z = Container([1,1,1,2,2,2,3,3,7,7,7,17])
    for i in Container(Z):
        if Z.count(i) > 1:
            Z.remove(i)
    print Z 
    print '[%s]' % min(X)    
    print '[%s]' % max(X) 
    print X.outinside(Y)
    print Y.outinside(X)
    X.union(Y)
    print X.union(X,Y)
    X.intersect(Y)
    print X.intersect(X,Y)
    print X | Y
    print X & Y 
    print X
    X.reverse(),
    print X
    print Y
    Y.reverse(),
    print Y
    Y.sort()
    print Y
    print X.insideout(Y)
    print Y.insideout(X)
    Z = Container ( [ "hello world","hello worl","hello wor","SE7EN"])
    W = Container ( [ "hello","Fouad Teniou","SE7EN","G"])
    print Z
    print W
    print Z & W
    a = Z | W
    a.reverse()
    print a
    print Z.insideout(W)
    print W.insideout(Z)
    print X & Y & W
    print X | Y | W
    G = Container('hello world')
    print G
    G & "try"
    print (G & "try")
    G | "try"
    print ( G | "try")

PS. There is no need to make Container as a subclass of list to be able to use the list commands such as reverse and sort... as it is mentioned in Python resourses, since list is a built in method and you can access it without having to use it as a super class 

-------------------------------------------------------------------
c:\hp\bin\Python>python "c:\hp\bin\Python\Scripts\Myscripts\Container2.py" 
<Container :  [1,2,3,7,17]
<Length : 5 
[1]
[6] 
<Container : [1,2,7,8,0]
<Length : 5
<Container : [7,8,0,1,2]
<Length : 5
<Container : [1,2,3,4,5,6,7,8,0]
<Length : 9
<Container : [1,2,3,4,5,6,7,8,0]
<Length : 9
<Container : [3,4,5,6]
<Length : 4
<Container : [3,4,5,6]
<Length : 4
<Container : [1,2,3,4,5,6]
<Length : 6
<Container : [6,5,4,3,2,1]
<Length : 6 
<Container : [3,4,5,6,7,8,0]
<Length : 7
<Container : [0,8,7,6,5,4,3]
<Length : 7 
<Container : [0,3,4,5,6,7,8]
<Length : 7 
<Container : [1,2]
<Length : 2 
<Container : [7,8,0]
<Length : 3 
<Container : ['hello world', 'hello word','hello wor','SE7EN']
<Length : 4 
<Container :['hello','Fouad Teniou','SE7EN','G']
<Length : 4
<Container : ['SE7EN']
<Length : 1
<Container : ['G','Fouad Teniou','hello','SE7EN','hello war','hello word','hello world']
<Length : 7
<Container : ['hello world','hello word','hello wor']
<Length : 3
<Container : ['hello','Fouad Teniou','G']
<Length : 3
<Container : []
<Length : 0
<Container : [1,2,3,4,5,6,0,7,8,'hello','Fouad Teniou','SE7EN','G']
<Length : 13
.......
..........
.........
...........

c:\hp\bin\Python>







  
