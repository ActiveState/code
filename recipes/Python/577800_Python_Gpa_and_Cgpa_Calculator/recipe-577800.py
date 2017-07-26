# @author: Abhijeet vaidya
# @contact: abhijeetavaidya@gmail.com
# @license: MIT license(Free Open Source License)
# @Description: Gpa is Grade point average, which is use to determine the student academic pointer 
#               based on the value of the grade he/she acquired in single semester, where as cgpa is cumlative 
#               grade point average is to calculate the total credits and total grade acquired in 
#               his/her entire academics. Here i have determined to use grade scale of two values
#               5.0 and 10.0, many other academics may have different grading system.For a different grades and   #               their grade values, You can change the value in method called getGradeData.For any bug report #               contact at above email-address

class Gpa(object):
    # data attributes
    "helps to calculate the Gpa and Cgpa"
    arg1 = None
    arg2 = None
    subData = None
    Scale = None
    credits = None
    initCourse = 0
    initgetCredit = 0
    totalCredits = 0
    temp = 0

    def getCourse(self):
        "get the value of the no of course you registered"
        self.arg1 = input("No of course you have registered: " )
        pass
    
    def getSubject(self,value):
        "get the subject value"
        self.arg2 = value
        pass
    
    def getScale(self):
        "To get the scale value"
        self.Scale = input("Enter the Scale value(Either 5 or 10): " )
        pass
        
        
    def getSubjectData(self):
        "get the subject Data in string"
        self.subData = raw_input("Enter the grade: " ) 
        pass              
    def getGradeData(self):
        # To calculate grade for two scale,one is for 5.0 and other one for 10.0
        if self.Scale == 10:
            
            grade1 = {'s':10,'a':9,'b':8,'c':7,'d':5,'e':3,'f':0}
            x=grade1[self.subData]
        
        else: #5.0 scale
            grade2 = {'a':5,'b':4,'c':3,'d':2,'e':1,'f':0}
            x=grade2[self.subData]
        return x 
    def getCredits(self):
        "get credit value"
        self.credits = input("Enter the credits for a subject:"  )
        pass
    
    def gpa(self):
        print "Calculate GPA:"
        sem = raw_input("Please Enter Semester: " )
        self.getScale() #input the scale value
        if self.Scale == 5 or self.Scale == 10:
            self.getCourse()
            if self.arg1 >= 2:
                self.calculateGpa()
            else:
                print "In order to calculate Gpa you schould have atleast 2 subject minimum"
        else:
            print "you have not entered the scale correctly please try again"
        pass
                
                
    def calculateGpa(self):
        "Method to calculate Gpa "
        while self.initCourse!=self.arg1:
            self.initCourse=self.initCourse+1
            self.getCredits()
            self.initgetCredit = self.credits
            self.getSubjectData()
            #type(self.getSubjectData())
            self.temp = self.initgetCredit*self.getGradeData()+self.temp
            self.totalCredits=self.totalCredits+self.initgetCredit
            
        gpa = round((self.temp+.0)/(self.totalCredits+.0),2)
        print "you have registered for total credits:"+" "+str(self.totalCredits)+" "+"and you have acquired GPA:\""+str(gpa)+"\""
        pass
    
    def cgpa(self):
        print "Calculate your cgpa: "
        semesters = input("Enter how many semester cgpa has to be found of: " )
        counter = 0
        tempInit = 0
        tempTotalCredits = 0
        self.getScale() #input the scale value
        if self.Scale == 5 or self.Scale == 10:
            while counter != semesters:
                counter = counter+1
                print "Please enter the details of the semester"+" "+str(counter)
                self.getCourse()
                self.calculateGpa()
                tempInit = self.temp+tempInit
                tempTotalCredits = tempTotalCredits + self.totalCredits
                # re-assigning
                self.arg1=0
                self.initCourse =0
                self.temp=0
                self.totalCredits=0
                print "\n"
                
            cgpa = round((tempInit+.0)/(tempTotalCredits+.0),2)
            
            print "you have registered for total credits:"+" "+str(tempTotalCredits)+" "+"and you have acquired CGPA:\""+str(cgpa)+"\" "    
        else:
            print "you have not entered the scale correctly please try again"
        pass


if __name__ == '__main__': # main method
    #how to calculate it

    Init = Gpa() # Creating Instance

    # for calculation of Cgpa (cumulative grade point average)
    Init.cgpa()

    # In Order to calculate Gpa for single semester
    #Init.gpa()
   

#output: 
"""
[abhi@localhost ~]$ python gpaCalculator.py

Calculate your cgpa: 
Enter how many semester cgpa has to be found of: 2
Enter the Scale value(Either 5 or 10): 10
Please enter the details of the semester 1
No of course you have registered: 2
Enter the credits for a subject:4
Enter the grade: a
Enter the credits for a subject:4
Enter the grade: c
you have registered for total credits: 8 and you have acquired GPA:"8.0"


Please enter the details of the semester 2
No of course you have registered: 3
Enter the credits for a subject:4
Enter the grade: b
Enter the credits for a subject:5
Enter the grade: a
Enter the credits for a subject:3
Enter the grade: c
you have registered for total credits: 12 and you have acquired GPA:"8.17"


you have registered for total credits: 20 and you have acquired CGPA:"8.1"     

"""
