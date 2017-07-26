# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria
#donyo@abv.bg
choice=None

def IM():

          

      num_0=input('Enter the number of plant parts with ball 0 (healthy): ')

      num_1=input('Enter the number of plant parts with ball 1: ')

      num_2=input('Enter the number of plant parts with ball 2: ')

      num_3=input('Enter the number of plant parts with ball 3: ')

      num_4=input('Enter the number of plant parts with ball 4: ')

      

      sumi=num_1+(2*num_2)+(3*num_3)+(4*num_4)

      sumg=num_0+num_1+num_2+num_3+num_4

      mb=0.00



      if num_1>0:

            mb=1

      if num_2>0:

            mb=2

      if num_3>0:

            mb=3

      if num_4>0:

            mb=4

          

      

      im=(float(sumi)/(sumg*mb))*100

      


      

      print \

            """

"""

      print "Index of Mc.Kynney: ", im

      print "General number of plant parts: ", sumg

                  

while choice!="0":

      print \

      """

     Index of Mc.Kynney Calculation Program

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             IM()











    





    

    



    









      

                      

                      





                      
