# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria

# donyo@abv.bg

import math

import datetime



choice=None

def air():

      f_y, f_m, f_d=input('Enter first date in format "year, month, day": ')

      s_y, s_m, s_d=input('Enter second date in format "year, month, day": ')

      f_pdi=float(input('Enter pdi observed at first date: '))

      s_pdi=float(input('Enter pdi observed at second date: '))



      f_date=datetime.date(f_y, f_m, f_d)

      s_date=datetime.date(s_y, s_m, s_d)

      sdif=str(s_date-f_date)

      int_dif=int(sdif[0:2])



      r=(1/float(int_dif))*math.log((s_pdi*(1-f_pdi))/(f_pdi*(1-s_pdi)))



      print \

            """

            """

      

      print "%2.10f" %r 

      

              

                        

while choice!="0":

      print \

      """

      Apparent Infection Rate Calculation



      Created by Donyo Ganchev - Agricultural University, Plovdiv, Bulgaria

      

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             air()
