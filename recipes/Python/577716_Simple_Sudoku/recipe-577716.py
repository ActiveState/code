 #<><><><><><><><><><><><><><><><><><><><><><><><> sodoko puzzle <><><><><><><><><><><><><><><><><><><><><><><><>
#  By : Amir Naghvi , Olempico@Gmail.com  #


import random

global Platform
global fill
Platform=[[0 for i in  "."*9]for i in "."*9] # Main table to Handle Game

class main(object):
    "------------- start --------------"
    def __init__(self):
        pass
    
    def gameloop(self): # ----------------GAME LOOP
        while True:
            o=raw_input('to show puzzle enter s to quit enter q: ')
            if o=="s":self.show()
            elif o=="q":return
            d=raw_input('first X then Y then NUM like  XyNumber (for example 245):  ')
            x=int(d[0]);y=int(d[1]);num=int(d[2])
            if self.give(x,y,num):
                print "True"
            else:
                print "you entered incorrect";
            self.show()
            
    def show(self): # -------To Printing puzzle
        c1=0
        c2=0
        for i in Platform:
            if c1%3==0:print" ->>"*21,
            print "     "
            c1+=1
            for j in i:
                c2+=1
                if j==0:
                    print " ","_ _"," ",
                    if c2%3==0:print r"|||",;
                else:
                    print " ",j," "," ",
                    if c2%3==0:print r"|||",;
            print "\n";
        print "\n\n";
            
    def give(self,x,y,NUM):  # ---for recieving number and it's position
        """ first checks if the position in not filled then change position's number
        then if the number is not valid changes the position number to 0 again and returns False"""
        
        if Platform[x-1][y-1]!=0:
            print"\n_________Already Filled__________\n";
            return False
        Platform [x-1][y-1]=NUM
        if not self.control(x,y):
            Platform [x-1][y-1]=0
            return False
        else:
            return True
            
    def control(slef,x,y):
        """There is Three checking stages:1st we find the number's row ,column and cube number then
        check if the row has not the same numbers  ,2nd we collect the number's colmn neigbours in 'colmns' list
        and simply do checking again 3rd: for checking the number in its cube area i explain below:"""
        row=x-1;#print row
        col=y-1;#print col
        
        # 1. row test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.1
        rows=[Platform[row][i] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if j!=i:
                    if rows[i]==rows[j] and rows[i]!=0 and rows[j]!=0:
                        if not fill:
                            print 'row'
                        return False
                        
        # 2. column test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.2
        colmns=[Platform[i][col] for i in range(9)]
        for i in range(9):
            for j in range(9):
                if j!=i:
                    if colmns[i]==colmns[j] and colmns[j]!=0 and colmns[i]!=0:
                        if not fill:
                            print 'col'
                        return False
                    
        # 3. 3x3 Cubes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.3
        """ 1.frst for 'first' cube number in X attitiude and sec second cube number in y ,for example centeral cube is (3,3)
        or first cube from bottom is (0,6) 2.then in 'cube' list i gather the cube numbers and 3.then simply check if there is a
        repeated numbers"""
        # 1.
        frst=-1
        sec=-1
        if row<3:frst=0
        elif row<6:frst=3
        elif row<9:frst=6
        if col<3:sec=0
        elif col<6:sec=3
        elif col<9:sec=6
        # 2.
        cube=[Platform[frst][sec+i]for i in range(3)] # creating cube
        cube.extend([Platform[frst+1][sec+i]for i in range(3)])
        cube.extend([Platform[frst+2][sec+i]for i in range(3)])
        # 3.
        for i in range(9):
            for j in range(9):
                if j!=i:
                    if cube[i]==cube[j] and cube[i]!=0 and cube[j]!=0:
                        if not fill:
                            print 'cube'
                        return False
        return True

    
        

# *********************************************************************
# *********************************************************************
if __name__=="__main__":
    o=main()                     # RUN
    o.gameloop()
# *********************************************************************
# *********************************************************************
