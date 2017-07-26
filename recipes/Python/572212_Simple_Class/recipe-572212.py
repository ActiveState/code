#---This is the class part---#
class Arit:
    def add(self,a,b):
        return a+b
    def subs(self,a,b):
        return a-b


#---This is the part that uses the class---#
n1=10
n2=4

operation=Arit()

print "The addition is", operation.add(n1,n2)

print "The substraction is", operation.subs(n1,n2)
