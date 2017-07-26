# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria

# donyo@abv.bg

import random



import numpy



choice=None

def menu():

      print \

      """

      Random test field design



      Created by Donyo Ganchev - Agricultural University, Plovdiv, Bulgaria

      

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             field()



def field():

      ntp=input('Enter number of test plants: ')

      nv=input('Enter number of plants in one test variant: ')

      npv=ntp/float(nv)

      print "Number of variants is: ", npv

      if npv != int(npv):

            print "Error ! The number of tests variants can not be fraction" 

            menu()



      else:

            row=input('Enter number of rows : ')

            col=input('Enter number of collums : ')

            

      prod=row*col

      plist=[0]*prod



      for i in range(prod):

           plist[i]=i+1

     

      random.shuffle(plist)

      from numpy import array

      a= array ([plist])

      b=a.reshape(col, row)

              

      print b

      

      

              

                        

while choice!="0":

      menu()
