 class gpa_cgpa(object):
      arg1 = None
      arg2 = None
      subdata = None
      credits = None
      init_course = 0
      init_credit =0
      total_credit =0
      temp = 0
      

      def getcourse(self):
          self.arg1 = input("No of course you have registered:")
          pass

      def getsubjectdata(self):
          self.subdata = raw_input("Enter the grade:")
          pass

      def getgradedata(self):
          grade = {'s':10,'a':9,'b':8,'c':7,'d':6,'e':5,'u':0,'i':0}
          x=grade[self.subdata]
          return x
     
      def getcredit(self):
          self.credits = input("Enter the credit for a subject :")
          pass

      def gpa(self):
          print "calculate GPA :"
          sem = raw_input("Enter the semester : ")
          self.getcourse()
          if self.arg1 >=2:
             self.calculateGpa()
          else:
            print " In order to calculate Gpa you should have atleast 2 subjects minimum"
          pass
      
      def calculateGpa(self):
          while self.init_course!=self.arg1:
              self.init_course=self.init_course+1
              self.getcredit()
              self.init_credit = self.credits
              self.getsubjectdata()
              self.temp = self.init_credit*self.getgradedata()+self.temp
              self.total_credit=self.total_credit+self.init_credit

          gpa = round((self.temp+0)/(self.total_credit+.0),2)
          print "you have registered for total credits:"+" "+str(self.total_credit)+" "+"and you have acquired GPA:\""+str(gpa)+"\""
          pass
    


      def cgpa(self):
          print  "Calculate your cgpa : "
          semester = input("Enter how many semester cgpa has to be found of :")
          counter =0
          tempinit = 0
          temptotalcredit =0 
          while counter!=semester:
                   counter = counter+1
                   print "Please enter the details of the semester"+" "+str(counter)
                   self.getcourse()
                   self.calculateGpa()
                   tempinit = self.temp+tempinit
                   temptotalcredit = temptotalcredit + self.total_credit
                # re-assigning
                   self.arg1=0
                   self.initCourse =0
                   self.temp=0
                   self.total_credits=0
                   print "\n"
                
          cgpa = round((tempinit+.0)/(temptotalcredit+.0),2)
            
          print "you have registered for total credits:"+" "+str(temptotalcredit)+" "+"and you have acquired CGPA:\""+str(cgpa)+"\" "
          pass


if __name__ == '__main__': # main method
    #how to calculate it

    Init = gpa_cgpa() # Creating Instance

    # for calculation of Cgpa (cumulative grade point average)
    Init.cgpa()

    # In Order to calculate Gpa for single semester
    #Init.gpa()
   


Calculate your cgpa: 
Enter how many semester cgpa has to be found of: 2
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
