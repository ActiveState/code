# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria
#donyo@abv.bg
choice=None

def H_T():

      num_liv_var_bt=input('Enter the number of live individuals in the variant before treatment : ')

      num_liv_var_at=input('Enter the number of live individuals in the variant after treatment: ')

      num_liv_con_bt=input('Enter number of live individuals in the control before treatment: ')

      num_liv_con_at=input('Enter number of live individuals in the control after treatment: ')



      eff=(1-((float(num_liv_con_bt)*num_liv_var_at)/(num_liv_con_at*num_liv_var_bt)))*100

         



      

      

      print \

            """

"""

      print "Effectiveness of the pesticide in % : ", eff

                        

while choice!="0":

      print \

      """

     Henderson and Tilton Calculation Program

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             H_T()











    





    

    



    









      

                      

                      





                      
