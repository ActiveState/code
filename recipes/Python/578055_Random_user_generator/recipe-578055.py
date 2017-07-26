'''Program to generate a random member from a list of users,
the members of the  default list can be removed or added to your convenience'''
import random,pickle,os#three of the modules used in the below code
g=os.getlogin()#gets the name of the computer
def adduser():#function definition for adding users to the list
    while 1==1:
        print(a)
        k=input('enter the name of the user(leave blank if none):')
        if k=='':
            break
        else:			
            a.append(k)
            f=open('random_members.data','wb')
            pickle.dump(a,f)
            f.close()
def deluser():#function definition for deleting users from the list
    while 1==1:
        print(a)
        k=input('enter the name of the user(leave blank if none):')
        if k=='':
            break
        else:
            for l in range(0,len(a)):
                if k==a[l-1]:
                    del a[l-1]
                    f=open('random_members.data','wb')
                    pickle.dump(a,f)
                    f.close
if os.path.isfile('C:\\Users'+os.sep+g+os.sep+'random_members.data') != True:#checking if the data file is already present in the computer, will make one if it is being run for the first time
    a=['warun','Morpheus3000','coolpcguy','David_007','fatalevolution','erif','[xubz]','GTX OC']#default list of members
    f=open('random_members.data','wb')
    pickle.dump(a,f)#dumps the default list
    f.close()
else:#this block grabs the list from the data file 
    f=open('random_members.data','rb')
    a=pickle.load(f)
    f.close()
y=input('would you like to add more users to the list y/n or press d to delete users:')
if y=='y':#block for adding users
    adduser()
    print(a)
    t=input('do you want to delete some users(y/n):')#provides one chance to remove some users
    if t=='y':
        deluser()#function call to delete users
        print('and the random member is',random.choice(a))
    else:
        print('and the random member is',random.choice(a))
elif y=='n':#quickest way to get an output
    print('and the random member is',random.choice(a))
elif y=='d':
    deluser()
    print(a)
    t=input('do you want to add new users(y/n):')#provides one chance to add some users
    if t=='y':
        adduser()#function call to add users
        print('and the random member is',random.choice(a))
    else:
        print('and the random member is',random.choice(a))
else:#this block is used if the input taken is unrecognisable however, I need to figure out a way to get it back to the beginning
    print('unrecognisable command')
