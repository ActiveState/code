#donyo@abv.bg
choice=None
def AUDPC():
      num_ob=input('Enter the number of observations: ')
      di=[0]*num_ob
      tim=[0]*num_ob
      index=0
      while index<num_ob:
                  di[index]=input('Enter the value of the Index of Makkiney: ')
                  index+=1
      index1=0
      while index1<num_ob:
                 tim[index1]=input('Enter the time of the observation in days: ')
                 index1=index1+1
                 meanvec=[0]*(num_ob-1)
                 intvec=[0]*(num_ob-1)

      x=0
      while x<(num_ob-1):
                meanvec[x]=(di[x]+di[x+1])/2
                x+=1

      y=0
      while y<(num_ob-1):
                  intvec[y]=tim[y+1]-tim[y]
                  y+=1

      sumvec=[meanvec[i]*intvec[i] for i in range(len(meanvec))]
      audpc=sum(sumvec)
      print \
            """"
"""
      print "AUDPC in percent-days: ", audpc
      r_audpc=audpc/max(tim)
      print "Relative AUDPC: ", r_audpc

while choice!="0":
      print \
      """
     AUDPC Calculation Program created by Donyo Ganchev
     1 - Begin calculation
     0 - Exit
     """
      choice= raw_input("Choice: ")
      if choice == "0":
                  exit()
      elif choice=="1":
             AUDPC ()





    


    
    

    




      
                      
                      


                      
