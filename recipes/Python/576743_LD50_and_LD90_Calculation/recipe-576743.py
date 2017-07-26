#donyo@abv.bg
from statlib import anova



choice=None

def ld():

      num_ob=input('Enter the number of observations: ')



      dose=[0]*num_ob

      response=[0]*num_ob

      

      index=0

      while index<num_ob:

                  print index+1

                  dose [index]=input('Enter the values of the doses: ')

                  index+=1

      print \

           """

     """

      index1=0

      while index1<num_ob:

            print index1+1

            response [index1]=input('Enter the values of the response (effectiveness): ')

            index1+=1



     

      res=anova.linregress(dose, response)

      ld50=(50-res[1])/res[0]

      ld90=(90-res[1])/res[0]

      

      

    

      print \

            """

      """

           

      print "R value is: ", res[2]

      print \

            """

      """

      print "LD 50 value is: ", ld50

      print "LD 90 value is: ", ld90

            



while choice!="0":

      print \

      """

     LD50 and LD90 Calculation Program



     Used module: Python - Statlib



     Created by Donyo Ganchev, Agricultural University, Plovdiv, Bulgaria

     

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             ld ()
