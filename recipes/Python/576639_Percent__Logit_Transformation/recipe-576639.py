# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria, donyo@abv.bg

import math

choice=None

def logit():

      per_eff=input('Enter percent of effectiveness : ')

      per_eff_tr=float(per_eff)/100

      lg=math.log(per_eff_tr/(1-per_eff_tr))

           

      

      print \

            """

"""

      print "Logit : ", lg

                        

while choice!="0":

      print \

      """

     Effectiveness -> Logit Calculation Program

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             logit()











    





    

    



    









      

                      

                      





                      
