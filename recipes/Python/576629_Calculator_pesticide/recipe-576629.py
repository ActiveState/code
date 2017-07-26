# Created by Donyo Ganchev, Agricultural University, town of Plovdiv, Bulgaria
#donyo@abv.bg
choice=None

def Concentration():

      per_act_sub=input('Enter the percent of active substance in formulation : ')

      per_con_ws=input('Enter the percent concentration of the pesticide solution: ')

      am_ws=input('Enter the amount of pesticide solution: ')



      m_val=(float(am_ws)/(((per_act_sub-per_con_ws)/10)+(per_con_ws/10)))

      am_pest_ws=(per_con_ws/10)*m_val

      am_water=(((per_act_sub-per_con_ws)/10)+(per_con_ws/10))*(am_ws)/(((per_act_sub-per_con_ws)/10)+(per_con_ws/10))-am_pest_ws

      

   
      

      print \

            """

"""

      print "Amount of pesticide formulation (ml or g): ", am_pest_ws

      print "Amount of water in pesticide solution (ml): ", am_water

                  

while choice!="0":

      print \

      """

     Pesticide Solution Concentration Program

     1 - Begin calculation

     0 - Exit

     """

      choice= raw_input("Choice: ")

      if choice == "0":

                  exit()

      elif choice=="1":

             Concentration()











    





    

    



    









      

                      

                      





                      
